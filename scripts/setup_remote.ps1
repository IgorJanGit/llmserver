# Quick Deploy Script for Remote Server
# Run this after transferring files to remote server

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Qwen LLM Server - Quick Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "1. Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if in correct directory
if (-not (Test-Path "..\main.py")) {
    Write-Host "   ✗ main.py not found. Are you in the llmServer\scripts directory?" -ForegroundColor Red
    Write-Host "   Run this from the project root instead: .\scripts\setup_remote.ps1" -ForegroundColor Yellow
    exit 1
}

# Change to project root
Set-Location ..

# Create models directory
Write-Host ""
Write-Host "2. Creating models directory..." -ForegroundColor Yellow
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
    Write-Host "   ✓ Created models/ directory" -ForegroundColor Green
} else {
    Write-Host "   ✓ models/ directory exists" -ForegroundColor Green
}

# Install dependencies
Write-Host ""
Write-Host "3. Installing dependencies..." -ForegroundColor Yellow
$installGPU = Read-Host "   Install with GPU support (CUDA)? (y/n)"

if ($installGPU -eq 'y') {
    Write-Host "   Installing llama-cpp-python with CUDA support..." -ForegroundColor Cyan
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
    pip install -r requirements.txt
} else {
    Write-Host "   Installing CPU version..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

# Check for model file
Write-Host ""
Write-Host "4. Checking for model file..." -ForegroundColor Yellow
if (Test-Path "models\qwen-14b.gguf") {
    Write-Host "   ✓ Model file found" -ForegroundColor Green
    $skipDownload = $true
} else {
    Write-Host "   ✗ Model file not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Download Qwen 14B GGUF model from:" -ForegroundColor Yellow
    Write-Host "   https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Recommended: qwen-14b-chat-q4_k_m.gguf (~8GB)" -ForegroundColor Yellow
    Write-Host "   Save as: models\qwen-14b.gguf" -ForegroundColor Yellow
    $skipDownload = $false
}

# Configure firewall
Write-Host ""
Write-Host "5. Configuring firewall..." -ForegroundColor Yellow
$configureFW = Read-Host "   Configure Windows Firewall to allow port 8000? (y/n)"

if ($configureFW -eq 'y') {
    try {
        # Check if running as admin
        $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if ($isAdmin) {
            New-NetFirewallRule -Name "QwenLLMServer" -DisplayName "Qwen LLM Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8000 -ErrorAction SilentlyContinue
            Write-Host "   ✓ Firewall rule added" -ForegroundColor Green
        } else {
            Write-Host "   ⚠ Need Administrator privileges for firewall" -ForegroundColor Yellow
            Write-Host "   Run this command as Administrator:" -ForegroundColor Yellow
            Write-Host "   New-NetFirewallRule -Name 'QwenLLMServer' -DisplayName 'Qwen LLM Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8000" -ForegroundColor Cyan
        }
    } catch {
        Write-Host "   ⚠ Could not configure firewall" -ForegroundColor Yellow
    }
}

# Get local IP
Write-Host ""
Write-Host "6. Network Information:" -ForegroundColor Yellow
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "127.*"} | Select-Object -First 1).IPAddress
if ($localIP) {
    Write-Host "   Local IP: $localIP" -ForegroundColor Green
    Write-Host "   Access server at: http://${localIP}:8000" -ForegroundColor Cyan
}

# Summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

if ($skipDownload) {
    Write-Host "✓ Ready to start server!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Start server:" -ForegroundColor Yellow
    Write-Host "  python main.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or run in background:" -ForegroundColor Yellow
    Write-Host "  python start_server_background.py" -ForegroundColor Cyan
    Write-Host ""
    
    $startNow = Read-Host "Start server now? (y/n)"
    if ($startNow -eq 'y') {
        Write-Host ""
        Write-Host "Starting server..." -ForegroundColor Green
        python main.py
    }
} else {
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Download model file (see above)" -ForegroundColor White
    Write-Host "2. Run: python main.py" -ForegroundColor White
}

Write-Host ""
