# Push the site to GitHub. Run from this folder:  .\push.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "-> " -NoNewline; git status --short | Measure-Object | ForEach-Object { Write-Host "$($_.Count) changed files" }

git add -A
$msg = Read-Host "Commit message (Enter = 'Update site')"
if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "Update site" }
git commit -m $msg
Write-Host "Pushing to GitHub — a browser window may open for sign-in..." -ForegroundColor Cyan
git push origin main
Write-Host "Done. GitHub Pages rebuilds in 1-5 minutes:" -ForegroundColor Green
Write-Host "  https://liangjinhao0213-sketch.github.io/weians-website/" -ForegroundColor Green
