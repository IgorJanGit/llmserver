# Remote Access Setup Guide

## SSH Access and Remote Testing

This guide helps you set up the Qwen LLM Server for remote access via SSH.

## Setup on Server Machine

### 1. Enable SSH on Windows (if not already enabled)

**Using PowerShell (Run as Administrator):**
```powershell
# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start the SSH service
Start-Service sshd

# Set it to start automatically
Set-Service -Name sshd -StartupType 'Automatic'

# Configure firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

### 2. Configure Firewall for LLM Server

```powershell
# Allow port 8000 for LLM Server
New-NetFirewallRule -Name "LLMServer" -DisplayName "LLM Server HTTP" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8000

# Or if using custom port (e.g., 8080)
New-NetFirewallRule -Name "LLMServer" -DisplayName "LLM Server HTTP" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8080
```

### 3. Find Your Server IP Address

```powershell
# Get local IP address
ipconfig

# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.1.100
```

### 4. Deploy the Server

```powershell
# 1. Copy project to server
# 2. Install dependencies
pip install -r requirements.txt

# 3. Download and place Qwen model in models/ folder

# 4. Start the server
python main.py

# Or run in background (recommended for remote)
python scripts/start_server_background.py
```

## Connect from Remote Computer

### Via SSH

```bash
# Connect to server
ssh username@192.168.1.100

# Navigate to project
cd C:\Users\Igorj\llmServer

# Check server status
python main.py

# Or test the server
python scripts\test_server.py
```

### Access API from Remote Computer

Once connected via SSH or on the same network:

```bash
# Test from remote machine
curl http://192.168.1.100:8000/health

# Or use Python
python
>>> import requests
>>> response = requests.get("http://192.168.1.100:8000/health")
>>> print(response.json())
```

## Remote Development Workflow

### Using VS Code Remote SSH

1. **Install VS Code Remote SSH Extension**
   - Open VS Code
   - Install "Remote - SSH" extension

2. **Connect to Server**
   - Press F1 → "Remote-SSH: Connect to Host"
   - Enter: `username@192.168.1.100`
   - Enter password when prompted

3. **Open Project**
   - File → Open Folder
   - Navigate to `C:\Users\Igorj\llmServer`

4. **Edit and Test Remotely**
   - Edit files directly on server
   - Run commands in integrated terminal
   - Test the server

### Using Git for Deployment

```bash
# On server - first time setup
cd C:\Users\Igorj\llmServer
git init
git add .
git commit -m "Initial commit"

# Push to remote repository (GitHub/GitLab)
git remote add origin <your-repo-url>
git push -u origin main

# On any computer - pull updates
ssh username@server-ip
cd C:\Users\Igorj\llmServer
git pull
```

## Security Considerations

### For Development/Testing (Local Network)

The current setup is fine for local network testing.

### For Production/Internet Access

If exposing to the internet, add these security measures:

1. **Add API Authentication:**

Create `auth_middleware.py`:
```python
from fastapi import HTTPException, Security, Header
from typing import Optional

API_KEY = "your-secret-api-key-here"

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key
```

Update `main.py`:
```python
from auth_middleware import verify_api_key

@app.post("/v1/chat/completions", dependencies=[Security(verify_api_key)])
async def chat_completion(request: CompletionRequest):
    ...
```

2. **Use HTTPS with SSL/TLS:**
```python
# In main.py main() function
uvicorn.run(
    app,
    host=host,
    port=port,
    ssl_keyfile="path/to/keyfile.pem",
    ssl_certfile="path/to/certfile.pem"
)
```

3. **Rate Limiting:**
```bash
pip install slowapi
```

4. **Use SSH Key Authentication (not password):**
```bash
# On client machine
ssh-keygen -t rsa -b 4096

# Copy public key to server
ssh-copy-id username@server-ip
```

## Testing Remote Access

### Quick Test Script

Save as `test_remote.py` on your local machine:

```python
import requests
import sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.100"
SERVER_PORT = 8000

print(f"Testing server at {SERVER_IP}:{SERVER_PORT}")

# Test health
try:
    response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/health")
    print(f"Health check: {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")
    sys.exit(1)

# Test completion
try:
    response = requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello!"}],
            "max_tokens": 50
        },
        timeout=60
    )
    print(f"Completion test: {response.json()}")
except Exception as e:
    print(f"Completion test failed: {e}")

print("\nRemote access is working!")
```

Run it:
```bash
python test_remote.py 192.168.1.100
```

## Troubleshooting Remote Access

### Cannot Connect via SSH

1. Check SSH service is running:
   ```powershell
   Get-Service sshd
   ```

2. Check firewall:
   ```powershell
   Get-NetFirewallRule -Name sshd
   ```

3. Verify IP address:
   ```powershell
   ipconfig
   ```

### Cannot Access LLM Server API

1. Check server is running:
   ```powershell
   # On server
   curl http://localhost:8000/health
   ```

2. Check firewall rule:
   ```powershell
   Get-NetFirewallRule -Name LLMServer
   ```

3. Test from server itself first:
   ```powershell
   curl http://localhost:8000/health
   ```

4. Then test from remote:
   ```bash
   curl http://SERVER_IP:8000/health
   ```

### Connection Refused

- Verify server is listening on `0.0.0.0` not `127.0.0.1`
- Check `config.json`: `"host": "0.0.0.0"`
- Restart the server after config changes

### Slow Performance Over Network

- Use a quantized model (Q4_K_M)
- Reduce `max_tokens` in requests
- Consider running model on GPU
- Check network bandwidth

## Port Forwarding (Internet Access)

If you need to access from outside your local network:

1. **Router Port Forwarding:**
   - Log into your router (usually 192.168.1.1)
   - Forward external port 8000 → internal IP:8000
   - Forward external port 22 → internal IP:22 (for SSH)

2. **Use Dynamic DNS:**
   - Sign up for services like No-IP or DuckDNS
   - Map your dynamic IP to a hostname

3. **Security:**
   - **REQUIRED**: Add authentication (API keys)
   - **REQUIRED**: Use HTTPS
   - **REQUIRED**: Use SSH keys (not passwords)
   - Consider VPN instead of direct exposure

## Alternative: Run as Windows Service

For production deployment, run as a service:

```powershell
# Install NSSM (Non-Sucking Service Manager)
# Download from: https://nssm.cc/

# Install as service
nssm install QwenLLM "C:\Users\Igorj\llmServer\dist\QwenLLMServer.exe"

# Start service
nssm start QwenLLM

# Server will auto-start on boot
```
