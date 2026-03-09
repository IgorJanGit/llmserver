# Quick Start Guide

## � 100% LOCAL - No Cloud, No API Keys

This server runs **completely locally** on your hardware. Your data never leaves your machine.

## �🚀 Get Started in 5 Minutes

### 1. Download Model (One Time Setup)

Download Qwen 14B GGUF model:
- Go to: https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF
- Download: `qwen-14b-chat-q4_k_m.gguf` (~8GB)
- Create `models` folder in project root
- Save as: `models/qwen-14b.gguf`

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

**For GPU support:**
```powershell
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

### 3. Start the Server

**Option A - Double-click (Windows):**
- Double-click `scripts/start_server.bat`

**Option B - Command line:**
```powershell
python main.py
```

**Option C - Background mode:**
```powershell
python scripts/start_server_background.py
```

### 4. Test It Works

Open browser: http://localhost:8000/docs

Or run test:
```powershell
python scripts/test_server.py
```

## 🌐 Remote Access

### Test from Another Computer

```powershell
# Replace 192.168.1.100 with your server IP
python scripts/test_remote.py 192.168.1.100
```

### Use the Client

```powershell
# Interactive chat
python client/client_example.py --server 192.168.1.100 --interactive

# Single query
python client/client_example.py --server 192.168.1.100 --prompt "Hello!"
```

**Note:** For SSH/firewall setup, use your existing SSH server configuration.

## 📁 Project Layout

```
llmServer/
├── main.py              # The server itself
├── config.json          # Settings
├── requirements.txt     # Dependencies
│
├── scripts/            # All helper scripts
│   ├── start_server.bat              # Quick start
│   ├── start_server_background.py    # Background mode
│   ├── stop_server.py                # Stop background
│   ├── test_server.py                # Test locally
│   ├── test_remote.py                # Test remotely
│   ├── verify_local_only.py          # Verify no cloud APIs
│   └── build_executable.py           # Build .exe
│
├── client/
│   └── client_example.py             # API client
│
├── docs/
│   ├── REMOTE_ACCESS.md              # Remote guide
│   └── DEPLOYMENT.md                 # Deploy guide
│
└── models/              # Put model here
    └── qwen-14b.gguf
```

## ⚙️ Configuration

Edit `config.json`:

```json
{
  "port": 8000,
  "model_path": "models/qwen-14b.gguf",
  "n_gpu_layers": -1,     // -1 = all GPU, 0 = CPU only
  "n_ctx": 4096,          // Context window
  "temperature": 0.7
}
```

## 🔧 Common Tasks

### Change Port
Edit `config.json`, change `"port": 8000` to desired port.

### Use CPU Only
Edit `config.json`, set `"n_gpu_layers": 0`

### Stop Background Server
```powershell
python scripts/stop_server.py
```

### Build Executable
```powershell
python scripts/build_executable.py
# Creates: dist/QwenLLMServer.exe
```

### View Logs
```powershell
type server_output.log
type server_error.log
```

## ❓ Troubleshooting

### Model Not Found
- Make sure model file is at `models/qwen-14b.gguf`
- Check `config.json` has correct path

### Out of Memory
- Set `"n_gpu_layers": 0` (use CPU)
- Set `"n_ctx": 2048` (reduce context)
- Use smaller model (Qwen-7B instead of 14B)

### Can't Connect Remotely
- Check firewall: `.\scripts\get_ip.ps1`
- Verify server is running: `python scripts/test_server.py`
- Test locally first: `curl http://localhost:8000/health`

### Port Already in Use
- Change port in `config.json`
- Or stop other service on port 8000

## 📚 More Information

- **Full Documentation**: [README.md](../README.md)
- **Remote Access**: [docs/REMOTE_ACCESS.md](docs/REMOTE_ACCESS.md)
- **Deployment**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 🎯 API Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "messages": [
            {"role": "user", "content": "Hello!"}
        ],
        "max_tokens": 100
    }
)

print(response.json()["content"])
```

## ✅ That's It!

You now have a local LLM server running. Access it at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

For remote access from other computers, see [docs/REMOTE_ACCESS.md](docs/REMOTE_ACCESS.md).
