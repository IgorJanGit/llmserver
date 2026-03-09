"""
Example client for interacting with the Qwen LLM Server
Use this from any computer that can reach the server

Usage:
    python client_example.py --server 192.168.1.100 --prompt "Hello, how are you?"
"""

import requests
import argparse
import json
from typing import List, Dict

class LLMClient:
    """Client for Qwen LLM Server"""
    
    def __init__(self, server_ip: str, port: int = 8000):
        self.base_url = f"http://{server_ip}:{port}"
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_server_info(self) -> dict:
        """Get server information"""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> dict:
        """Get model information"""
        response = self.session.get(f"{self.base_url}/model/info")
        response.raise_for_status()
        return response.json()
    
    def chat(
        self,
        message: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        conversation_history: List[Dict] = None
    ) -> tuple:
        """
        Send a chat message to the server
        
        Returns:
            (response_text, usage_dict)
        """
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add user message
        messages.append({"role": "user", "content": message})
        
        # Make request
        response = self.session.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=120  # 2 minutes timeout
        )
        
        response.raise_for_status()
        data = response.json()
        
        return data["content"], data.get("usage", {})
    
    def chat_interactive(self, system_prompt: str = None):
        """Interactive chat session"""
        print("="*60)
        print("Interactive Chat Session")
        print("Type 'quit' or 'exit' to end session")
        print("Type 'clear' to clear history")
        print("="*60)
        print()
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'clear':
                    conversation_history = []
                    print("Conversation history cleared.")
                    continue
                
                # Get response
                print("Assistant: ", end='', flush=True)
                response, usage = self.chat(
                    user_input,
                    system_prompt=system_prompt,
                    conversation_history=conversation_history
                )
                print(response)
                
                # Add to history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Show token usage
                if usage:
                    print(f"\n[Tokens: {usage.get('total_tokens', 'N/A')}]")
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Try again or type 'quit' to exit\n")

def main():
    parser = argparse.ArgumentParser(description="Qwen LLM Server Client")
    parser.add_argument("--server", required=True, help="Server IP address")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--prompt", help="Single prompt to send")
    parser.add_argument("--system", help="System prompt")
    parser.add_argument("--interactive", action="store_true", help="Start interactive session")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature (0.0-2.0)")
    parser.add_argument("--max-tokens", type=int, default=500, help="Max tokens in response")
    parser.add_argument("--info", action="store_true", help="Show server info")
    
    args = parser.parse_args()
    
    # Create client
    client = LLMClient(args.server, args.port)
    
    # Check connection
    print(f"Connecting to server at {args.server}:{args.port}...")
    if not client.health_check():
        print("❌ Server is not reachable!")
        print("Make sure:")
        print(f"  - Server is running on {args.server}:{args.port}")
        print("  - Firewall allows connections")
        print("  - IP address is correct")
        return 1
    
    print("✅ Connected!")
    print()
    
    # Show server info
    if args.info:
        try:
            info = client.get_server_info()
            print("Server Information:")
            print(json.dumps(info, indent=2))
            print()
            
            model_info = client.get_model_info()
            print("Model Information:")
            print(json.dumps(model_info, indent=2))
            print()
        except Exception as e:
            print(f"Error getting info: {e}")
        return 0
    
    # Interactive mode
    if args.interactive:
        client.chat_interactive(system_prompt=args.system)
        return 0
    
    # Single prompt mode
    if args.prompt:
        try:
            print("Sending prompt...")
            response, usage = client.chat(
                args.prompt,
                system_prompt=args.system,
                temperature=args.temperature,
                max_tokens=args.max_tokens
            )
            
            print()
            print("Response:")
            print("-" * 60)
            print(response)
            print("-" * 60)
            
            if usage:
                print(f"\nTokens used: {usage.get('total_tokens', 'N/A')}")
            
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    # No mode specified, show help
    print("Usage examples:")
    print()
    print("  # Single prompt:")
    print(f"  python client_example.py --server {args.server} --prompt \"What is Python?\"")
    print()
    print("  # With system prompt:")
    print(f"  python client_example.py --server {args.server} --system \"You are a helpful coding assistant\" --prompt \"Write a hello world in Python\"")
    print()
    print("  # Interactive chat:")
    print(f"  python client_example.py --server {args.server} --interactive")
    print()
    print("  # Server info:")
    print(f"  python client_example.py --server {args.server} --info")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())
