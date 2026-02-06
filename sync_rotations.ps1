# Auto-elevate to Administrator if not already running as admin
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Requesting administrator privileges..." -ForegroundColor Yellow
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
    exit
}

$source = "C:\Kod\munkey\Rotations"
$target = "E:\Dropbox_20050140\QuickTimePlayer_25071748\230126031555"

Write-Host "Syncing rotations from:" -ForegroundColor Cyan
Write-Host "  Source: $source" -ForegroundColor Gray
Write-Host "  Target: $target" -ForegroundColor Gray
Write-Host ""

$count = 0

# Find all rotation yaml files and create symlinks
Get-ChildItem -Path $source -Recurse -Filter "*.yaml" | 
Where-Object { $_.Name -like "*rotation*" } |
ForEach-Object {
    $linkPath = Join-Path $target $_.Name
    if (Test-Path $linkPath) { Remove-Item $linkPath -Force }
    New-Item -ItemType SymbolicLink -Path $linkPath -Target $_.FullName | Out-Null
    Write-Host "  Linked: $($_.Name)" -ForegroundColor Green
    $count++
}

Write-Host ""
Write-Host "Done! Created $count symlinks." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")