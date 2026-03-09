# Qwen 14B Local LLM Server

**🔒 100% LOCAL - NO Cloud APIs, NO API Keys, Complete Privacy**

A standalone HTTP server for running Qwen 14B **completely locally** on your own hardware. Can be packaged as an executable file.

## 🛡️ Privacy & Security

- ✅ **Runs 100% locally** - All inference on your hardware
- ✅ **No cloud APIs** - No OpenAI, Anthropic, or external services
- ✅ **No API keys needed** - Completely self-contained
- ✅ **Complete privacy** - Your data never leaves your machine
- ✅ **Works offline** - No internet required after model download

📖 **See [docs/LOCAL_ONLY.md](docs/LOCAL_ONLY.md) for complete privacy & security details**

## 🚀 Quick Start for Remote Access

**On Server:**
```powershell
# 1. Setup (automated)
.\scripts\setup_remote.ps1

# 2. Get your IP address
.\scripts\get_ip.ps1

# 3. Start server in background
python scripts\start_server_background.py
```

**From Any Computer:**
```bash
# Test connection (replace with your server IP)
python scripts/test_remote.py 192.168.1.100

# Or use the API
curl http://192.168.1.100:8000/health
```

**Via SSH:**
```bash
ssh username@192.168.1.100
cd C:\Users\Igorj\llmServer
python main.py
```

📖 **Full remote access guide:** [docs/REMOTE_ACCESS.md](docs/REMOTE_ACCESS.md)  
📋 **Deployment checklist:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)  
⚡ **Quick start guide:** [QUICKSTART.md](QUICKSTART.md)  
📁 **Project structure:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)  
🔒 **Privacy & local-only info:** [docs/LOCAL_ONLY.md](docs/LOCAL_ONLY.md)

## Features

- ✅ **100% Local Operation** - NO cloud APIs, NO data leaves your machine
- ✅ **No API keys required** - Completely self-contained
- ✅ Run Qwen 14B model locally on your hardware
- ✅ HTTP API for LLM completions
- ✅ GPU acceleration support (CUDA/Metal)
- ✅ FastAPI with automatic API documentation
- ✅ Can be packaged as a standalone .exe file
- ✅ CORS enabled for web applications
- ✅ Optimized with llama.cpp backend
- ✅ Works completely offline after model download

### 🔍 Verify Local-Only Operation

Run the verification script to confirm no cloud dependencies:

```powershell
python scripts/verify_local_only.py
```

This checks:
- ✅ No cloud API imports in code
- ✅ No cloud packages in requirements.txt
- ✅ No API keys in config.json
- ✅ Local inference library (llama-cpp-python) present

## Quick Start (Local)

### Step 1: Download Qwen 14B Model

Download the GGUF format model from HuggingFace:

**Option A - Recommended (Quantized, smaller & faster):**
```bash
# Create models directory
mkdir models

# Download Q4_K_M quantized version (~8GB)
# Go to: https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF
# Download: qwen-14b-chat-q4_k_m.gguf
# Save it to: models/qwen-14b.gguf
```

**Option B - Full precision (larger, slower):**
```bash
# Download full F16 version (~28GB)
# Follow same steps but download: qwen-14b-chat-f16.gguf
```

### Step 2: Install Dependencies

**For GPU support (NVIDIA):**
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
pip install -r requirements.txt
```

**For CPU only:**
```bash
pip install -r requirements.txt
```

**For Mac (Metal GPU):**
```baBuild the executable:**
   ```bash
   python build_executable.py
   ```

2. **Setup for distribution:**
   ```
   dist/
   ├── QwenLLMServer.exe
   ├── config.json
   └── models/
       └── qwen-14b.gguf
   ```

3. **Run the executable:**
   ```bash
   cd dist
   QwenLLMServer.exe
   ```

The executable will be created in the `dist` folder. Make sure to include the models folder!
Settings:
- `n_gpu_layers`: `-1` for all GPU, `0` for CPU only
- `n_ctx`: Context window size (4096 works well)
- `n_threads`: CPU threads to use

### Step 4: Run the Server

```bash
pyttemperature": 0.7,
  "max_tokens": 500,
  "top_p": 0.95
}
```

Response:
```json
{
  "content": "I'm doing well, thank you! How can I help you today?",
  "model": "qwen-14b
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   python build_executable.py
   ```

3. **Run the executable:**
   ```bash
   dist\LLMServer.exe
   ```

The executable will be created in the `dist` folder.

## API Usage

### Chat Completion Endpoint

**POST** `/v1/chat/completions`

Request body:
```json
{
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

Response:
```json
{
  "content": "I'm doing well, thank you! How can I help you today?",
  "model": "qwen-14b",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 15,
    "total_tokens": 27
  }
}
```

### Example with cURL

```bashExplain quantum computing in simple terms.\"}], \"max_tokens\": 500}"
```

### Example with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
)

print(response.json()["content"])
```

### Example with System Prompt

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
   model_path": "models/qwen-14b.gguf",
  "n_ctx": 4096,
  "n_gpu_layers": -1,
  "n_threads": 4,
  "max_tokens": 2000,
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "repeat_penalty": 1.1,
  "verbose": false
}
```

### Configuration Options

- **model_path**: Path to the GGUF model file
- **n_ctx**: Context window size (max tokens in context)
- **n_gpu_layers**: Number of layers to offload to GPU
  - `-1`: Use all GPU layers (fastest)
  - `0`: CPU only (slower but works everywhere)
  - `20-40`: Partial offload (balance GPU memory usage)
- **n_threads**: CPU threads for processing
- **temperature**: Randomness (0.0-2.0, higher = more creative)
- **top_p**: Nucleus sampling (0.0-1.0)
- **top_k**: Top-K sampling (number of tokens to consider)
- **repeat_penalty**: Penalty for repeating tokens (1.0 = no penalty)

### Performance Tuning

**For best performance on GPU:**
```json
├── test_server.py         # Test suite
├── README.md             # This file
└── models/
    └── qwen-14b.gguf      # Qwen model (download separately)
```

### Using Different Models

This server uses llama.cpp backend, so it works with any GGUF model:

**Other Qwen models:**
- Qwen-7B (smaller, faster)
- Qwen-72B (larger, better quality)

**OtModel Not Found Error

```
FileNotFoundError: Model not found at models/qwen-14b.gguf
```

**Solution:** Download the model and place it in the `models/` folder. See Step 1 above.

### Out of Memory Error

**For GPU:**
- Reduce `n_gpu_layers` (try 20-30 instead of -1)
- Reduce `n_ctx` (try 2048 instead of 4096)
- Use a smaller quantized model (Q4_K_M instead of F16)

**For CPU:**
- Set `n_gpu_layers: 0`
- Reduce `n_ctx` to 2048 or 1024
- Consider using Qwen-7B instead of 14B

### Slow Performance

**Solutions:**
1. Make sure GPU layers are enabled: `"n_gpu_layers": -1`
2. Install GPU-accelerated llama-cpp-python (see installation)
3. Use a quantized model (Q4_K_M is 4x faster than F16)
4. Reduce `n_ctx` if you don't need long context

### Port Already in Use

Change the port in `config.json`:
```json
{
  "port": 8080
}
```

### Windows Defender Blocking Executable

- Add exception for the .exe file
- Or run from source with `python main.py# config.json

```json
{
  "host": "0.0.0.0",
  "port": 8000,
  "default_provider": "openai",
  "openai_api_key": "",
  "anthropic_api_key": "",
  "max_tokens": 2000,
  "temperature": 0.7
}
```

### Supported Providers

- **OpenAI**: GPT-3.5, GPT-4, etc.
  - Models: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo-preview`
  
- **Anthropic**: Claude models
  - Models: `claude-3-sonnet-20240229`, `claude-3-opus-20240229`, `claude-3-haiku-20240307`

## Development

### Project Structure

```
llmServer/
├── main.py                 # Main server application
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── build_executable.py    # Build script for creating .exe
└── README.md             # This file
```

### Adding New Providers

To add a new LLM provider:

1. Add the provider's library to `requirements.txt`
2. Create a completion function in `main.py` (e.g., `async def newprovider_completion()`)
3. Add the provider case in the `/v1/chat/completions` endpoint
4. Update the config.json with provider-specific settings

## Troubleshooting

### Executable Issues

If the executable doesn't run:
- Make sure `config.json` is in the same directory as the .exe
- Check Windows Defender/antivirus isn't blocking it
- Run from command prompt to see error messages

### Model Issues

- Verify model file exists at path specified in `config.json`
- Check model file is not corrupted (re-download if needed)
- Ensure model is in GGUF format (not PyTorch .bin or .safetensors)

### Port Already in Use

If port 8000 is already in use, change it in `config.json`:
```json
{
  "port": 8080
}
```

## Remote Access & SSH

This server is designed for easy remote access and deployment:

### Quick Remote Setup

1. **On Server Machine:**
   ```powershell
   # Run automated setup
   .\scripts\setup_remote.ps1
   ```

2. **Enable SSH Access:**
   ```powershell
   # Install OpenSSH Server (as Administrator)
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   Start-Service sshd
   Set-Service -Name sshd -StartupType 'Automatic'
   ```

3. **Configure Firewall:**
   ```powershell
   # Allow LLM Server port
   New-NetFirewallRule -Name "QwenLLMServer" -DisplayName "Qwen LLM Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 8000
   ```

4. **From Remote Computer:**
   ```bash
   # Test connection
   python scripts/test_remote.py 192.168.1.100
   
   # Or use SSH helper
   .\scripts\ssh_connect.ps1
   ```

### Background Server Mode

For remote deployment, run server in background:

```powershell
# Start in background
python scripts/start_server_background.py

# Check status
python scripts/test_server.py

# Stop server
python scripts/stop_server.py
```

### VS Code Remote SSH

1. Install "Remote - SSH" extension in VS Code
2. Press F1 → "Remote-SSH: Connect to Host"
3. Enter: `username@server-ip`
4. Open folder: `C:\Users\Igorj\llmServer`
5. Edit and test directly on remote server!

### Access from Other Computers

```python
import requests

# Replace with your server's IP
response = requests.post(
    "http://192.168.1.100:8000/v1/chat/completions",
    json={
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 200
    }
)

print(response.json()["content"])
```

For detailed instructions, see **[REMOTE_ACCESS.md](REMOTE_ACCESS.md)**

## License

MIT License - Feel free to use and modify as needed.
