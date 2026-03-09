# Deployment Checklist for Qwen LLM Server

## Pre-Deployment

- [ ] Python 3.8+ installed
- [ ] Download Qwen 14B GGUF model (~8GB for Q4_K_M)
- [ ] At least 16GB RAM (32GB recommended for 14B model)
- [ ] NVIDIA GPU with 8GB+ VRAM (optional but recommended)

## Server Setup

### 1. Install Dependencies

- [ ] Run: `pip install -r requirements.txt`
- [ ] For GPU support: `pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121`

### 2. Model Setup

- [ ] Create `models/` directory
- [ ] Download Qwen model from HuggingFace
- [ ] Rename to `models/qwen-14b.gguf`
- [ ] Verify file size (~8GB for Q4_K_M)

### 3. Configuration

- [ ] Edit `config.json`:
  - [ ] Set `model_path` correctly
  - [ ] Set `n_gpu_layers` (-1 for GPU, 0 for CPU)
  - [ ] Set `n_ctx` (4096 recommended)
  - [ ] Set `host` to "0.0.0.0" for network access
  - [ ] Set `port` (default 8000)

### 4. Network Setup

- [ ] Run `.\get_ip.ps1` to find server IP
- [ ] Configure Windows Firewall:
  ```powershell
  New-NetFirewallRule -Name "QwenLLMServer" -DisplayName "Qwen LLM Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8000
  ```
- [ ] Note server IP address for remote access



## Testing

### Local Testing

- [ ] Start server: `python main.py`
- [ ] Wait for model to load (can take 30-60 seconds)
- [ ] Run tests: `python test_server.py`
- [ ] Check http://localhost:8000/docs

### Remote Testing

- [ ] From another computer: `python scripts/test_remote.py [SERVER_IP]`
- [ ] Try API call with curl or Python requests
- [ ] Verify firewall allows connections

## Production Deployment

### Background Mode

- [ ] Start server: `python scripts/start_server_background.py`
- [ ] Verify running: Check `server_output.log`
- [ ] Test connection: `python scripts/test_server.py`
- [ ] Stop server: `python scripts/stop_server.py`

### Executable Deployment

- [ ] Build exe: `python scripts/build_executable.py`
- [ ] Copy `dist/QwenLLMServer.exe` to deployment location
- [ ] Copy `config.json` to same directory as exe
- [ ] Copy `models/` folder to same directory as exe
- [ ] Run executable
- [ ] Verify functionality

## Security (For Internet Access)

**⚠️ Only if exposing to internet:**

- [ ] Add API key authentication
- [ ] Configure HTTPS/SSL
- [ ] Set up rate limiting

- [ ] Configure router port forwarding
- [ ] Consider VPN instead of direct exposure
- [ ] Regular security updates

## Monitoring

- [ ] Check `server_output.log` for errors
- [ ] Check `server_error.log` for crashes
- [ ] Monitor GPU/CPU usage
- [ ] Monitor memory usage
- [ ] Monitor disk space (models are large)

## Common Commands

### Start Server
```powershell
# Foreground
python main.py

# Background
python scripts/start_server_background.py
```

### Stop Server
```powershell
# If in background
python scripts/stop_server.py

# If in foreground
Ctrl+C
```

### Check Status
```powershell
# Local
python scripts/test_server.py

# Remote
python scripts/test_remote.py [SERVER_IP]
```

### View Logs
```powershell
# Output log
type server_output.log

# Error log
type server_error.log

# Live tail (requires PowerShell 7+)
Get-Content server_output.log -Wait
```

## Troubleshooting

### Model Won't Load
- [ ] Check file path in config.json
- [ ] Verify model file exists and isn't corrupted
- [ ] Check you have enough RAM
- [ ] Try reducing `n_ctx` value

### Out of Memory
- [ ] Reduce `n_gpu_layers`
- [ ] Reduce `n_ctx` to 2048
- [ ] Use smaller quantized model (Q4 instead of Q8)
- [ ] Close other applications

### Can't Connect Remotely
- [ ] Verify server is running: `python test_server.py`
- [ ] Check firewall rules: `Get-NetFirewallRule -Name "QwenLLMServer"`
- [ ] Test from server first: `curl http://localhost:8000/health`
- [ ] Ping server from remote computer

### Slow Performance
- [ ] Enable GPU: Set `n_gpu_layers: -1`
- [ ] Install GPU-accelerated llama-cpp-python
- [ ] Use quantized model (Q4_K_M)
- [ ] Reduce `max_tokens` in requests
- [ ] Reduce `n_ctx`

## Support

- Documentation: See README.md
- Privacy/Local-Only: See docs/LOCAL_ONLY.md
- Test Scripts: Use scripts/test_server.py and scripts/test_remote.py
- Configuration: Edit config.json
