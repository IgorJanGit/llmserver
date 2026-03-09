#!/usr/bin/env pwsh
# Quick Start Script for PowerShell
# Usage: .\START_HERE.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Qwen LLM Server - 100% LOCAL MODELS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔒 Privacy: NO cloud APIs, NO API keys" -ForegroundColor Green
Write-Host "   Your data stays on YOUR machine!" -ForegroundColor Green
Write-Host ""

# Check if model exists
if (-not (Test-Path "models\qwen-14b.gguf")) {
    Write-Host "⚠️  Model not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please download Qwen 14B model first:" -ForegroundColor White
    Write-Host "1. Create 'models' folder" -ForegroundColor Gray
    Write-Host "2. Download from: https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF" -ForegroundColor Gray
    Write-Host "3. Save as: models\qwen-14b.gguf" -ForegroundColor Gray
    Write-Host ""
    Write-Host "See QUICKSTART.md for detailed instructions" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""
Write-Host "Starting server..." -ForegroundColor Green
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor White
Write-Host "  • http://localhost:8000" -ForegroundColor Cyan
Write-Host "  • http://localhost:8000/docs (API documentation)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python main.py
