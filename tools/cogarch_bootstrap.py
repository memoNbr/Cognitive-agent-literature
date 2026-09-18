#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cogarch_bootstrap.py — minimal BDI cognitive agent for ANY OpenAI-compatible endpoint.

Boots a belief-desire-intention loop: beliefs from perception, desires scored per goal,
the strongest valid desire committed as an intention, then acted on and reflected.
Carries priors + memory JSON persistence, a configurable sampling cadence, a trust/
confidence score over samples, and a generic "act" hook you override with your tools.

Config (env or --config ini, [cogarch] section): COGARCH_BASE_URL (default
http://localhost:11434/v1 — works with ollama/llama.cpp/vLLM/OpenAI), COGARCH_API_KEY
(default "none"), COGARCH_MODEL.  Use --demo for a 3-cycle offline stub, no API needed.
"""
import argparse
import configparser
import json
import os
import sys
import time
import urllib.request

DEFAULTS = {
    "base_url": "http://localhost:11434/v1",
    "api_key": "none",
    "model": "qwen2.5:7b",
}


def load_config(args):
    cfg = dict(DEFAULTS)
    if args.config and os.path.isfile(args.config):
        p = configparser.ConfigParser()
        p.read(args.config)
        for k in cfg:
            if p.has_option("cogarch", k):
                cfg[k] = p.get("cogarch", k)
    for k in cfg:  # env overrides ini
        env = os.environ.get("COGARCH_" + k.upper())
        if env:
            cfg[k] = env
    for k in ("model", "base_url", "api_key"):  # CLI wins over everything
        v = getattr(args, k, None)
        if v:
            cfg[k] = v
    return cfg


def llm_call(cfg, messages, temperature=0.4):
    """Blocking chat-completions call. Returns the assistant text or None on failure."""
    body = json.dumps({
        "model": cfg["model"],
        "messages": messages,
        "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(
        url=cfg["base_url"].rstrip("/") + "/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + cfg["api_key"],
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
    except Exception as exc:  # network / malformed reply / timeout
        sys.stderr.write("llm_call failed: %s\n" % exc)
        return None


class StubBackend(object):
    """Deterministic, offline stand-in for an OpenAI endpoint (used by --demo)."""

    def respond(self, cfg, messages):
        latest = messages[-1]["content"]
        if "goal" in latest:
            return "I commit to the goal and will act on it now."
        return "Cycle hypothesis noted; continuing observation and reflection."


class CogAgent(object):
    """A job of that old friend, the BDI loop, in ~70 lines."""

    GOALS = {
        "observe": {"pre": lambda self: True, "desire": lambda self, obs: 0.5},
        "explain": {"pre": lambda self: bool(self.beliefs.get("primes")),
                    "desire": lambda self, obs: 0.8},
        "decide":  {"pre": lambda self: True, "desire": lambda self, obs: 0.9},
    }

    def __init__(self, cfg, state_path, act_fn=None, backend=None):
        self.cfg = cfg
        self.state_path = state_path
        self.backend = backend or self  # plug a StubBackend for offline runs
        self.beliefs = {}
        self.intention = None
        self.intention_since = 0.0
        self.last_fired = {}
        self.memory = []
        self.samples = []
        self.priors = self._load() or {"rides": 0, "trust": 0.5}
        self.trust = self.priors["trust"]
        self.act_fn = act_fn or self.default_act

    # ---- persistence ---------------------------------------------------
    def _load(self):
        try:
            with open(self.state_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return None

    def save(self):
        blob = {
            "priors": self.priors, "beliefs": self.beliefs,
            "memory": self.memory[-8:], "samples": self.samples,
            "intention": self.intention,
        }
        with open(self.state_path, "w", encoding="utf-8") as fh:
            json.dump(blob, fh, indent=2)

    # ---- perception / memory -------------------------------------------
    def perceive(self, observation):
        self.beliefs["primes"] = sorted(set(observation.lower().split()))[:8]
        self.memory.append({"t": time.time(), "obs": observation})
        self.memory = self.memory[-8:]

    def react(self, text):
        print("  agent : %s" % text)

    # ---- BDI loop -------------------------------------------------------
    def cycle(self, observation):
        self.perceive(observation)
        best, best_v = None, 0.0
        now = time.time()
        for name, goal in self.GOALS.items():
            if not goal["pre"](self):
                continue
            if now - self.last_fired.get(name, 0.0) < 1.5:  # cooldown
                continue
            value = goal["desire"](self, observation)
            if value > best_v:
                best, best_v = name, value
        was = self.intention
        self.intention = best
        if best and best != was:
            self.last_fired[best] = now
            self.intention_since = now
            self.reflect("intend", best)  # tell the model, then act
        self.act_fn(best, observation, self)
        sample = self.sample()
        self.update_trust(sample)
        return best

    # ---- act hook (override me) -----------------------------------------
    def default_act(self, intention, observation, agent):
        if intention:
            text = self.backend.respond(self.cfg, [
                {"role": "system", "content": "You are the deliberator of a BDI agent."},
                {"role": "user", "content": "goal: %s | state: %s" % (intention, observation)},
            ])
            agent.react(text or "[no model reply]")

    def reflect(self, verb, what):
        text = self.backend.respond(self.cfg, [
            {"role": "system", "content": "You are briefly told what the agent is doing."},
            {"role": "user", "content": "%s: %s" % (verb, what)},
        ])
        if text:
            print("  cycle: %s %s" % (verb, what))

    # ---- sampling + trust -------------------------------------------------
    def sample(self):
        s = {"t": time.time(), "conf": min(1.0, 0.5 + 0.05 * len(self.samples))}
        self.samples.append(s)
        return s

    def update_trust(self, s):
        # priors-weighted EWMA: new evidence 60%, carried priors 40%
        self.trust = 0.6 * s["conf"] + 0.4 * (self.priors.get("trust", 0.5))
        self.priors["rides"] = self.priors.get("rides", 0) + 1
        self.priors["trust"] = round(self.trust, 3)


def demo_act(intention, observation, agent):
    """Scriptable stub used by --demo: deterministic, no network needed."""
    canned = {
        "observe": "Scanning surroundings; logging what is new.",
        "explain": "Mapping discovered primes into a tentative account.",
        "decide": "Committing to the strongest desire as the next intention.",
        None: "Idle — no valid desire above threshold this cycle.",
    }
    print("  act   : %s" % canned.get(intention, canned[None]))


def make_user_act(name):
    """Allow --act module.func without third-party imports; fallback to demo."""
    if not name or name == "demo_act":
        return demo_act
    try:
        mod, _, fn = name.partition(".")
        import importlib
        return getattr(importlib.import_module(mod), fn or "act")
    except Exception:
        sys.stderr.write("could not import act hook %r — using demo.\n" % name)
        return demo_act


def main(argv=None):
    p = argparse.ArgumentParser(description="Boot a minimal cognitive agent.")
    p.add_argument("--config", help="optional .ini with [cogarch] base_url/api_key/model")
    p.add_argument("--base_url")
    p.add_argument("--api_key")
    p.add_argument("--model")
    p.add_argument("--cycles", type=int, default=3, help="number of BDI cycles")
    p.add_argument("--cadence", type=float, default=0.2, help="seconds between cycles")
    p.add_argument("--state", default="cogarch_state.json", help="priors/memory JSON file")
    p.add_argument("--act", default="demo_act",
                   help="act hook: module.func or a built-in demo (offline)")
    p.add_argument("--demo", action="store_true",
                   help="3-cycle pass with a scriptable stub — no real API, offline-safe")
    args = p.parse_args(argv)
    cfg = load_config(args)
    backend = StubBackend() if args.demo else None
    act = demo_act if args.demo else make_user_act(args.act)
    agent = CogAgent(cfg, args.state, act_fn=act, backend=backend)
    print("boot  : %s @ %s | cycles=%d cadence=%gs trust0=%.2f"
          % (cfg["model"], cfg["base_url"], args.cycles, args.cadence, agent.trust))
    demos = [
        "new section spotted while patrolling the corridor",
        "repeated pattern is present in the sensor feed",
        "anomaly reoccurs; pattern strengthens",
    ]
    for i in range(args.cycles):
        print("cycle %d/%d:" % (i + 1, args.cycles))
        intention = agent.cycle(demos[min(i, len(demos) - 1)])
        print("  trust : %.3f | intent=%s" % (agent.trust, intention))
        time.sleep(args.cadence)
    agent.save()
    print("done  : %d cycles | state persisted -> %s | trust=%.3f"
          % (args.cycles, args.state, agent.trust))
    return 0


if __name__ == "__main__":
    sys.exit(main())