# Get local IP addresses for network access
# Run this on the server to find out how to connect to it
# Usage: .\scripts\get_ip.ps1 or from root: .\scripts\get_ip.ps1

$adapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*"}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Server Network Information" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

if ($adapters.Count -eq 0) {
    Write-Host "No network adapters found!" -ForegroundColor Red
    Write-Host "Make sure you're connected to a network." -ForegroundColor Yellow
    exit
}

Write-Host "Your IP Addresses:" -ForegroundColor Yellow
Write-Host ""

foreach ($adapter in $adapters) {
    $interface = Get-NetAdapter -InterfaceIndex $adapter.InterfaceIndex
    Write-Host "  Interface: $($interface.Name)" -ForegroundColor White
    Write-Host "  IP Address: $($adapter.IPAddress)" -ForegroundColor Green
    Write-Host "  Status: $($interface.Status)" -ForegroundColor Cyan
    Write-Host ""
}

# Get the primary IP (usually the first non-loopback)
$primaryIP = $adapters[0].IPAddress

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "From other computers, access your server at:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  http://$primaryIP:8000" -ForegroundColor Green -BackgroundColor DarkGray
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Yellow
Write-Host "  Health:     http://$primaryIP:8000/health" -ForegroundColor White
Write-Host "  Docs:       http://$primaryIP:8000/docs" -ForegroundColor White
Write-Host "  Model Info: http://$primaryIP:8000/model/info" -ForegroundColor White
Write-Host "  Chat API:   http://$primaryIP:8000/v1/chat/completions" -ForegroundColor White
Write-Host ""

Write-Host "SSH Access:" -ForegroundColor Yellow
Write-Host "  ssh $env:USERNAME@$primaryIP" -ForegroundColor White
Write-Host ""

Write-Host "Test from remote computer:" -ForegroundColor Yellow
Write-Host "  python test_remote.py $primaryIP" -ForegroundColor White
Write-Host ""

# Check if SSH is enabled
$sshService = Get-Service -Name sshd -ErrorAction SilentlyContinue

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Service Status:" -ForegroundColor Yellow
Write-Host ""

if ($sshService) {
    if ($sshService.Status -eq "Running") {
        Write-Host "  SSH Server: ✓ Running" -ForegroundColor Green
    } else {
        Write-Host "  SSH Server: ✗ Not Running" -ForegroundColor Red
        Write-Host "  Start with: Start-Service sshd" -ForegroundColor Yellow
    }
} else {
    Write-Host "  SSH Server: ✗ Not Installed" -ForegroundColor Red
    Write-Host "  Install with: Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0" -ForegroundColor Yellow
}

# Check firewall status
$fwRule = Get-NetFirewallRule -Name "QwenLLMServer" -ErrorAction SilentlyContinue

if ($fwRule) {
    Write-Host "  Firewall:   ✓ Port 8000 allowed" -ForegroundColor Green
} else {
    Write-Host "  Firewall:   ⚠ Not configured" -ForegroundColor Yellow
    Write-Host "  Configure with: New-NetFirewallRule -Name 'QwenLLMServer' -DisplayName 'Qwen LLM Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8000" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Copy connection string to clipboard if available
try {
    Set-Clipboard -Value "python test_remote.py $primaryIP"
    Write-Host "✓ Test command copied to clipboard!" -ForegroundColor Green
    Write-Host ""
} catch {
    # Clipboard not available, no problem
}
