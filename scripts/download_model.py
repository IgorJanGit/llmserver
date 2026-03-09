#!/usr/bin/env python3
"""Download Qwen3-14B model from HuggingFace"""

import os
from huggingface_hub import hf_hub_download

print("\n" + "="*50)
print("  Downloading Qwen2.5-14B GGUF Model")
print("="*50 + "\n")

print("Model: Qwen2.5-14B-Instruct Q4_K_M (~8.5 GB)")
print("Location: X:\\LLM_Models\\")
print("Source: Qwen/Qwen2.5-14B-Instruct-GGUF\n")

# Ensure directory exists
os.makedirs("X:\\LLM_Models", exist_ok=True)

# Try different repositories and filenames
repos_to_try = [
    ("Qwen/Qwen2.5-14B-Instruct-GGUF", "qwen2.5-14b-instruct-q4_k_m.gguf"),
    ("Qwen/Qwen2.5-14B-Instruct-GGUF", "Qwen2.5-14B-Instruct-Q4_K_M.gguf"),
    ("Qwen/Qwen-14B-Chat-GGUF", "qwen-14b-chat-q4_k_m.gguf"),
]

downloaded_file = None
for repo_id, filename in repos_to_try:
    try:
        print(f"Trying {repo_id}/{filename}...")
        
        downloaded_file = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir="X:\\LLM_Models",
            local_dir_use_symlinks=False
        )
        print(f"✓ Found and downloading from {repo_id}")
        break
    except Exception as e:
        print(f"  Not found in {repo_id}")
        continue

if downloaded_file:
    try:
        # Rename to qwen-14b.gguf as configured in config.json
        target_path = "X:\\LLM_Models\\qwen-14b.gguf"
        if os.path.exists(downloaded_file) and downloaded_file != target_path:
            if os.path.exists(target_path):
                os.remove(target_path)
            os.rename(downloaded_file, target_path)
            print(f"\n✓ Download complete!")
            print(f"✓ Renamed to: {target_path}")
        else:
            print(f"\n✓ Download complete!")
            print(f"✓ Saved to: {downloaded_file}")
        
        # Show file size
        if os.path.exists(target_path):
            size_gb = os.path.getsize(target_path) / (1024**3)
            print(f"✓ File size: {size_gb:.2f} GB")
            
            print("\n" + "="*50)
            print("  Ready to use!")
            print("="*50)
            print("\nTest the server with:")
            print("  python main.py")
            print("\n")
        
    except Exception as e:
        print(f"\n✗ Error during file operations: {e}")

else:
    print("\n✗ Could not find model in any known repository")
    print("\nAlternative: Download manually from:")
    print("  https://huggingface.co/Qwen/Qwen3-14B-Instruct-GGUF")
    print("  Or: https://huggingface.co/Qwen/Qwen3-14B")
    print("  Save as: X:\\LLM_Models\\qwen-14b.gguf")
