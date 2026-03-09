"""
Stop the background LLM server
"""

import os
import sys
import signal
from pathlib import Path

def stop_server():
    """Stop the background server"""
    
    # Look for PID file in parent directory
    pid_file = Path(__file__).parent.parent / 'server.pid'
    
    if not pid_file.exists():
        print("No server PID file found.")
        print("Server may not be running, or was started differently.")
        return
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        print(f"Stopping server with PID: {pid}")
        
        if sys.platform == 'win32':
            # Windows
            import subprocess
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
        else:
            # Unix-like
            os.kill(pid, signal.SIGTERM)
        
        # Remove PID file
        pid_file.unlink()
        
        print("✅ Server stopped successfully")
        
    except ProcessLookupError:
        print("Process not found. Server may have already stopped.")
        pid_file.unlink()
    except Exception as e:
        print(f"Error stopping server: {e}")
        print(f"Try manually killing process {pid}")

if __name__ == "__main__":
    stop_server()
