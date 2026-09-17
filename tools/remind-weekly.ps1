# Weekly reminder for the Cognitive Agent Literature repo.
# Fires 1 day before the weekly review (scheduled Sunday 09:00, review Monday).
# Shows a Windows toast; falls back to a WinForms popup if toast fails.
#
# The message includes the repo path, the newest edition, and how fresh it is.

$repo = "C:\Users\Win11 Pro\Memo\cognitive-agent-literature"
$repoUrl = "https://github.com/memoNbr/cognitive-agent-literature"

$latest = Get-ChildItem "$repo\editions\*.md" | Sort-Object Name -Descending | Select-Object -First 1
$latestName = if ($latest) { $latest.BaseName } else { "none yet" }
$daysSince = 0
if ($latest) {
    $daysSince = [int](New-TimeSpan -Start $latest.LastWriteTime.Date -End (Get-Date).Date).TotalDays
}

$title = "Cognitive Agent Literature - weekly review tomorrow"
$msg = "New edition is due tomorrow (Monday).`nRepo: $repoUrl`nLast edition: $latestName ($daysSince day(s) ago).`nLook it up and present the new version - tell cond to have mind refresh."

function Show-Toast($t, $m) {
    try {
        Add-Type -AssemblyName System.Runtime.WindowsRuntime
        $null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime]
        $null = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType=WindowsRuntime]
        $asTaskType = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
            $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
            $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
        })[0]
        $tray = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Cognitive Agent Literature")
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml("<toast><visual><binding template='ToastGeneric'><text>$t</text><text>$($m -replace '<','&lt;' -replace '>','&gt;')</text></binding></visual></toast>")
        $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
        $tray.Show($toast)
        return $true
    } catch {
        return $false
    }
}

if (-not (Show-Toast $title $msg)) {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $f = New-Object Windows.Forms.Form
    $f.Text = $title
    $f.StartPosition = 'CenterScreen'
    $f.Size = New-Object Drawing.Size(560, 220)
    $l = New-Object Windows.Forms.Label
    $l.Text = ($msg -replace "`n", "`n")
    $l.AutoSize = $true
    $l.Location = New-Object Drawing.Point(16, 16)
    $f.Controls.Add($l)
    $f.TopMost = $true
    $f.ShowDialog() | Out-Null
}