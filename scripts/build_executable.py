"""
Build script to create standalone executable
Run: python scripts/build_executable.py
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build():
    """Build the executable using PyInstaller"""
    
    # Get paths
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    main_py = root_dir / "main.py"
    config_file = root_dir / "config.json"
    
    # PyInstaller arguments
    args = [
        str(main_py),                       # Main script
        '--name=QwenLLMServer',             # Name of the executable
        '--onefile',                        # Create a single executable file
        '--console',                        # Show console window
        f'--add-data={config_file};.',      # Include config file
        '--hidden-import=uvicorn.logging',  # Hidden imports
        '--hidden-import=uvicorn.loops',
        '--hidden-import=uvicorn.loops.auto',
        '--hidden-import=uvicorn.protocols',
        '--hidden-import=uvicorn.protocols.http',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.lifespan.on',
        '--hidden-import=llama_cpp',
        '--collect-all=uvicorn',
        '--collect-all=fastapi',
        '--collect-all=llama_cpp',
        '--noconfirm',                      # Replace output directory without asking
    ]
    
    print("Building executable...")
    print("This may take a few minutes...")
    
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*60)
    print("Build complete!")
    print("="*60)
    print(f"Executable created at: dist\\QwenLLMServer.exe")
    print("\nBefore running:")
    print("1. Download Qwen 14B GGUF model")
    print("2. Create a 'models' folder next to the .exe")
    print("3. Place the model file as models/qwen-14b.gguf")
    print("\nThen run: dist\\QwenLLMServer.exe")

if __name__ == "__main__":
    build()
