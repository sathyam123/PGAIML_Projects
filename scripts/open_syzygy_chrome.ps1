param(
    [string]$Url = "https://www.syzygyai.in/",
    [switch]$Incognito,
    [switch]$NewWindow
)

# Common Chrome install locations on Windows
$chromePaths = @(
    "$Env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "$Env:ProgramFiles(x86)\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromePaths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($chrome) {
    $args = @()
    if ($Incognito) { $args += "--incognito" }
    if ($NewWindow) { $args += "--new-window" }
    $args += $Url
    Start-Process -FilePath $chrome -ArgumentList $args
} else {
    Write-Host "Google Chrome not found in the usual locations. Opening default browser instead..."
    Start-Process $Url
}
