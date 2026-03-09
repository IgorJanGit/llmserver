# Qwen 14B LLM Server - Project Structure

## Overview
This project is organized into logical folders for easy navigation and deployment.

## Directory Structure

```
llmServer/
│
├── main.py                  # Main server application
├── config.json              # Server configuration
├── requirements.txt         # Python dependencies
├── README.md               # Main documentation
├── .gitignore              # Git ignore rules
│
├── scripts/                # All utility scripts
│   ├── start_server.bat            # Quick start (Windows)
│   ├── start_server_background.py  # Run server in background
│   ├── stop_server.py              # Stop background server
│   ├── test_server.py              # Test local server
│   ├── test_server.bat             # Quick test (Windows)
│   ├── test_remote.py              # Test from remote computer
│   ├── verify_local_only.py        # Verify no cloud APIs
│   └── build_executable.py         # Build standalone .exe
│
├── client/                 # Client libraries and examples
│   └── client_example.py           # Full-featured API client
│
├── docs/                   # Documentation
│   ├── LOCAL_ONLY.md               # Privacy & local-only info
│   └── DEPLOYMENT.md               # Deployment checklist
│
└── models/                 # Model files (not included)
    └── qwen-14b.gguf              # Download separately
```

## Runtime Files (Created Automatically)

```
├── server_output.log      # Server output logs
├── server_error.log       # Server error logs
├── server.pid             # Server process ID (background mode)
├── dist/                  # Built executable (after running build)
└── build/                 # Build artifacts
```

## Quick Reference

### Starting the Server

```powershell
# From project root - Quick start
.\scripts\start_server.bat

# Python - Foreground
python main.py

# Python - Background
python scripts\start_server_background.py
```

### Testing

```powershell
# Local testing
python scripts\test_server.py

# Remote testing (replace IP)
python scripts\test_remote.py 192.168.1.100
```



### Client Usage

```bash
# Interactive chat
python client/client_example.py --server 192.168.1.100 --interactive

# Single query
python client/client_example.py --server 192.168.1.100 --prompt "Hello!"
```

### Building Executable

```bash
python scripts/build_executable.py
# Creates: dist/QwenLLMServer.exe
```

## File Purposes

### Core Files (Root)
- **main.py** - FastAPI server, model loading, API endpoints
- **config.json** - All server settings (model path, GPU config, etc.)
- **requirements.txt** - All Python package dependencies

### Scripts Folder
- **Server Management** - start/stop server, run in background
- **Testing** - Test both local and remote connections
- **Setup & Deployment** - Automated setup, IP detection, SSH helpers
- **Build** - Create standalone executable

### Client Folder
- **client_example.py** - Feature-complete Python client with:
  - Single prompt mode
  - Interactive chat mode
  - Server info queries
  - Conversation history

### Documentation Folder
- **REMOTE_ACCESS.md** - Complete guide for SSH, remote access, security
- **DEPLOYMENT.md** - Step-by-step deployment checklist

## Import Paths

All scripts are designed to work from the project root:

```powershell
# From project root (recommended)
python scripts/test_server.py
python client/client_example.py --server localhost

# Scripts handle paths automatically
```

## Configuration

All configuration is in `config.json` at project root. Scripts will find it automatically.

## Logs and Runtime Data

All runtime files (logs, PIDs) are created in the project root for easy access.
