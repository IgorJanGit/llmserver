# SSH Quick Connection Script
# Edit SERVER_IP to your remote server's IP address
# Usage: .\scripts\ssh_connect.ps1

$SERVER_IP = "192.168.1.100"  # Change this to your server IP
$SERVER_USER = $env:USERNAME   # Default to current username
$PROJECT_PATH = "C:\Users\Igorj\llmServer"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  SSH Connection Helper" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Menu
Write-Host "1. Connect to server via SSH" -ForegroundColor Yellow
Write-Host "2. Copy files to server (SCP)" -ForegroundColor Yellow
Write-Host "3. Test server connection" -ForegroundColor Yellow
Write-Host "4. View server logs" -ForegroundColor Yellow
Write-Host "5. Configure settings" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "Select option (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Connecting to $SERVER_USER@$SERVER_IP..." -ForegroundColor Green
        ssh "$SERVER_USER@$SERVER_IP" "cd $PROJECT_PATH; powershell"
    }
    
    "2" {
        Write-Host "Copying files to server..." -ForegroundColor Green
        scp -r * "$SERVER_USER@${SERVER_IP}:$PROJECT_PATH"
        Write-Host "Files copied!" -ForegroundColor Green
    }
    
    "3" {
        Write-Host "Testing server connection..." -ForegroundColor Green
        python test_remote.py $SERVER_IP 8000
    }
    
    "4" {
        Write-Host "Fetching server logs..." -ForegroundColor Green
        ssh "$SERVER_USER@$SERVER_IP" "cd $PROJECT_PATH; type server_output.log"
    }
    
    "5" {
        $newIP = Read-Host "Enter server IP address [$SERVER_IP]"
        if ($newIP) {
            $content = Get-Content $PSCommandPath
            $content = $content -replace "SERVER_IP = `".*`"", "SERVER_IP = `"$newIP`""
            Set-Content $PSCommandPath $content
            Write-Host "Updated server IP to: $newIP" -ForegroundColor Green
        }
        
        $newUser = Read-Host "Enter username [$SERVER_USER]"
        if ($newUser) {
            Write-Host "Username set to: $newUser" -ForegroundColor Green
            $SERVER_USER = $newUser
        }
    }
    
    default {
        Write-Host "Invalid option" -ForegroundColor Red
    }
}

Write-Host ""
