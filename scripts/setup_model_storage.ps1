# Setup Model Storage on X: Drive
# Creates folder structure and prepares for model download

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Model Storage Setup" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Create models folder on X: drive
$modelPath = "X:\LLM_Models"

Write-Host "Creating model storage folder..." -ForegroundColor Cyan
if (-not (Test-Path $modelPath)) {
    New-Item -Path $modelPath -ItemType Directory -Force | Out-Null
    Write-Host "  OK Created: $modelPath" -ForegroundColor Green
}
else {
    Write-Host "  OK Folder already exists: $modelPath" -ForegroundColor Green
}

# Show download instructions
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Next: Download Qwen 14B Model" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Recommended quantization (8 GB):" -ForegroundColor White
Write-Host "  https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF/blob/main/qwen-14b-chat-q4_k_m.gguf" -ForegroundColor Gray

Write-Host "`nOther options:" -ForegroundColor White
Write-Host "  - Q5_K_M (10 GB, better quality):" -ForegroundColor Gray
Write-Host "    https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF/blob/main/qwen-14b-chat-q5_k_m.gguf" -ForegroundColor DarkGray
Write-Host "  - Q8_0 (14 GB, best quality):" -ForegroundColor Gray
Write-Host "    https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF/blob/main/qwen-14b-chat-q8_0.gguf" -ForegroundColor DarkGray

Write-Host "`nDownload steps:" -ForegroundColor Cyan
Write-Host "  1. Click the link above" -ForegroundColor White
Write-Host "  2. Click download button on HuggingFace page" -ForegroundColor White
Write-Host "  3. Save to: $modelPath" -ForegroundColor White
Write-Host "  4. Rename to: qwen-14b.gguf" -ForegroundColor White

Write-Host "`nOr use command line:" -ForegroundColor Cyan
Write-Host "  cd $modelPath" -ForegroundColor Gray
Write-Host "  Invoke-WebRequest -Uri 'https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF/resolve/main/qwen-14b-chat-q4_k_m.gguf' -OutFile 'qwen-14b.gguf'" -ForegroundColor Gray

# Check current space on X:
$xDrive = Get-PSDrive X -ErrorAction SilentlyContinue
if ($xDrive) {
    $freeGB = [math]::Round($xDrive.Free / 1GB, 2)
    Write-Host "`nOK X: drive has $freeGB GB free (plenty of space!)" -ForegroundColor Green
}

Write-Host "`nAfter download, test with:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor Gray
Write-Host ""
