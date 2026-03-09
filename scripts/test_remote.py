"""
Test remote server connection
Usage: python test_remote.py [server_ip] [port]
Example: python test_remote.py 192.168.1.100 8000
"""

import requests
import sys
import json
from typing import Optional

def test_remote_server(server_ip: str, port: int = 8000):
    """Test connection to remote LLM server"""
    
    base_url = f"http://{server_ip}:{port}"
    
    print("="*60)
    print(f"Testing Remote LLM Server: {base_url}")
    print("="*60)
    print()
    
    # Test 1: Health check
    print("1. Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ {response.json()}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to {base_url}")
        print("   Check:")
        print("   - Server is running")
        print("   - Firewall allows port", port)
        print("   - IP address is correct")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    print()
    
    # Test 2: Server info
    print("2. Server Info...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Model: {data.get('model')}")
            print(f"   Model Loaded: {data.get('model_loaded')}")
            print(f"   Model Path: {data.get('model_path')}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 3: Model info (if loaded)
    print("3. Model Information...")
    try:
        response = requests.get(f"{base_url}/model/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Model: {data.get('model')}")
            print(f"   Context Length: {data.get('context_length')}")
            print(f"   GPU Layers: {data.get('gpu_layers')}")
            print(f"   ✅ Model loaded and ready")
        elif response.status_code == 503:
            print(f"   ⚠️  Model not loaded")
            return True  # Server is running but model not loaded
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  {e}")
    print()
    
    # Test 4: Config
    print("4. Configuration...")
    try:
        response = requests.get(f"{base_url}/config", timeout=5)
        if response.status_code == 200:
            config = response.json()
            print(f"   Host: {config.get('host')}")
            print(f"   Port: {config.get('port')}")
            print(f"   Max Tokens: {config.get('max_tokens')}")
            print(f"   Temperature: {config.get('temperature')}")
    except Exception as e:
        print(f"   ⚠️  {e}")
    print()
    
    # Test 5: Completion (if model is loaded)
    print("5. Testing Completion Endpoint...")
    try:
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": "Say only 'OK' and nothing else."}
                ],
                "max_tokens": 20,
                "temperature": 0.1
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Response: {data.get('content')}")
            usage = data.get('usage', {})
            print(f"   Tokens: {usage.get('total_tokens')} total")
        elif response.status_code == 503:
            print(f"   ⚠️  Model not loaded - skipping completion test")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Error: {response.json()}")
    except requests.exceptions.Timeout:
        print(f"   ⚠️  Request timed out (model still loading or slow)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    print("="*60)
    print("Remote server test complete!")
    print("="*60)
    return True

def get_local_ip():
    """Get local network IP addresses"""
    import socket
    try:
        # Get hostname
        hostname = socket.gethostname()
        # Get IP
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return None

if __name__ == "__main__":
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python test_remote.py [server_ip] [port]")
        print("\nExamples:")
        print("  python test_remote.py 192.168.1.100")
        print("  python test_remote.py 192.168.1.100 8000")
        
        # Try to help with local IP
        local_ip = get_local_ip()
        if local_ip:
            print(f"\nYour local IP appears to be: {local_ip}")
            print(f"If testing locally, try: python test_remote.py {local_ip}")
        
        sys.exit(1)
    
    server_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    
    success = test_remote_server(server_ip, port)
    sys.exit(0 if success else 1)
