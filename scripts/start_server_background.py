"""
Background server starter - runs the LLM server as a background process
Useful for remote deployment and long-running sessions
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def is_server_running(port=8000):
    """Check if server is already running"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def start_server_background():
    """Start the server in background"""
    
    # Check if already running
    if is_server_running():
        print("Server is already running on port 8000")
        print("To stop it, use: stop_server.py")
        return
    
    # Determine if running from source or executable
    if getattr(sys, 'frozen', False):
        # Running as executable
        cmd = [sys.executable]
    else:
        # Running from source
        main_path = Path(__file__).parent.parent / "main.py"
        cmd = [sys.executable, str(main_path)]
    
    print("Starting LLM Server in background...")
    
    # Get root directory
    root_dir = Path(__file__).parent.parent
    log_dir = root_dir
    
    # Start process in background
    if sys.platform == 'win32':
        # Windows - use CREATE_NO_WINDOW flag
        CREATE_NO_WINDOW = 0x08000000
        process = subprocess.Popen(
            cmd,
            stdout=open(log_dir / 'server_output.log', 'w'),
            stderr=open(log_dir / 'server_error.log', 'w'),
            creationflags=CREATE_NO_WINDOW,
            cwd=str(root_dir)
        )
    else:
        # Unix-like systems
        process = subprocess.Popen(
            cmd,
            stdout=open(log_dir / 'server_output.log', 'w'),
            stderr=open(log_dir / 'server_error.log', 'w'),
            start_new_session=True,
            cwd=str(root_dir)
        )
    
    # Save PID for later
    with open(root_dir / 'server.pid', 'w') as f:
        f.write(str(process.pid))
    
    print(f"Server started with PID: {process.pid}")
    print("Waiting for server to initialize...")
    
    # Wait for server to start
    max_wait = 30
    for i in range(max_wait):
        time.sleep(1)
        if is_server_running():
            print("\n✅ Server is running!")
            print(f"   - API: http://localhost:8000")
            print(f"   - Docs: http://localhost:8000/docs")
            print(f"   - Logs: server_output.log, server_error.log")
            print(f"   - PID: {process.pid}")
            print("\nTo stop the server, run: python stop_server.py")
            return
        print(f".", end='', flush=True)
    
    print("\n⚠️  Server may still be starting up. Check server_output.log for details.")
    print("This may take a few minutes if loading a large model.")

if __name__ == "__main__":
    start_server_background()
