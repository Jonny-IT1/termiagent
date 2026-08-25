# 🚀 TermiAgent One-Liner Installer (Windows PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "📦 Installing TermiAgent via uv..." -ForegroundColor Cyan

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv package manager..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:PATH = "$HOME\.local\bin;" + $env:PATH
}

uv pip install -e .

Write-Host ""
Write-Host "🎉 TermiAgent installation complete!" -ForegroundColor Green
Write-Host "Run 'termiagent' in any terminal to start chatting with your codebase." -ForegroundColor Yellow
