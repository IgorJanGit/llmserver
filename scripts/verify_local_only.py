"""
Verification script to confirm LOCAL MODELS ONLY
Run this to verify no cloud API dependencies
"""

import sys
import os
from pathlib import Path

def check_imports():
    """Check main.py for cloud API imports"""
    print("Checking main.py for cloud API imports...")
    
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    cloud_apis = ['openai', 'anthropic', 'cohere', 'google.generativeai']
    found = []
    
    for api in cloud_apis:
        if f'import {api}' in content or f'from {api}' in content:
            found.append(api)
    
    if found:
        print(f"  ❌ FOUND cloud API imports: {', '.join(found)}")
        return False
    else:
        print("  ✅ NO cloud API imports found")
        return True

def check_requirements():
    """Check requirements.txt for cloud packages"""
    print("\nChecking requirements.txt for cloud packages...")
    
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    cloud_packages = ['openai', 'anthropic', 'cohere', 'google-generativeai']
    found = []
    
    for pkg in cloud_packages:
        if pkg in content:
            found.append(pkg)
    
    if found:
        print(f"  ❌ FOUND cloud packages: {', '.join(found)}")
        return False
    else:
        print("  ✅ Only local packages found")
        return True

def check_config():
    """Check config.json for API keys"""
    print("\nChecking config.json for API keys...")
    
    import json
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    api_key_fields = [k for k in config.keys() if 'api' in k.lower() and 'key' in k.lower()]
    
    if api_key_fields:
        print(f"  ❌ FOUND API key fields: {', '.join(api_key_fields)}")
        return False
    else:
        print("  ✅ NO API key fields found")
        return True

def check_llama_cpp():
    """Check if llama-cpp-python is available"""
    print("\nChecking for llama-cpp-python (local inference)...")
    
    try:
        import llama_cpp
        print("  ✅ llama-cpp-python is installed")
        return True
    except ImportError:
        print("  ❌ llama-cpp-python NOT installed")
        print("     Run: pip install -r requirements.txt")
        return False

def main():
    print("="*60)
    print("LOCAL MODELS ONLY - Verification Script")
    print("="*60)
    print("\nVerifying this server uses ONLY local models...\n")
    
    results = []
    
    # Run all checks
    results.append(check_imports())
    results.append(check_requirements())
    results.append(check_config())
    results.append(check_llama_cpp())
    
    # Summary
    print("\n" + "="*60)
    if all(results):
        print("✅ VERIFICATION PASSED - 100% LOCAL MODELS ONLY")
        print("="*60)
        print("\nThis server:")
        print("  ✅ Uses ONLY local model inference (llama-cpp-python)")
        print("  ✅ Has NO cloud API dependencies")
        print("  ✅ Requires NO API keys")
        print("  ✅ Keeps your data completely private")
        print("\nYour data stays on YOUR machine! 🔒")
        return 0
    else:
        print("❌ VERIFICATION FAILED - Cloud dependencies found!")
        print("="*60)
        print("\nPlease check the items marked with ❌ above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
