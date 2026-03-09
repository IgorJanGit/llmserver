"""
Test script for the LLM Server
Run this after starting the server to verify it's working
"""

import requests
import json

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get("http://localhost:8000/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_completion():
    """Test chat completion endpoint"""
    print("Testing chat completion with Qwen 14B...")
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": "Say 'Hello World' and nothing else."}
                ],
                "max_tokens": 50,
                "temperature": 0.3
            },
            timeout=60  # Longer timeout for model inference
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response content: {result['content']}")
            print(f"Usage: {json.dumps(result.get('usage', {}), indent=2)}")
        else:
            print(f"Error: {response.json()}")
    except requests.exceptions.Timeout:
        print("Request timed out - model might still be loading or inference is slow")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_config():
    """Test config endpoint"""
    print("Testing config endpoint...")
    response = requests.get("http://localhost:8000/config")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_model_info():
    """Test model info endpoint"""
    print("Testing model info endpoint...")
    try:
        response = requests.get("http://localhost:8000/model/info")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("="*60)
    print("Qwen 14B LLM Server Test Suite")
    print("="*60)
    print("Make sure the server is running on http://localhost:8000")
    print("And the Qwen model is loaded!\n")
    
    try:
        test_health()
        test_root()
        test_config()
        test_model_info()
        test_completion()
        
        print("="*60)
        print("Tests complete!")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the server is running: python main.py")
        
        print("="*60)
        print("Tests complete!")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the server is running: python main.py")
