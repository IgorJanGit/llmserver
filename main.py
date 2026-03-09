"""
LLM Server - A local model server supporting multiple models
Can be packaged as a standalone executable
Supports: Qwen, Llama 3.1, and other GGUF models
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import json
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import llama-cpp-python for local model inference
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

# Configuration
class Config:
    def __init__(self):
        self.config_file = self._get_config_path()
        self.load_config()
    
    def _get_config_path(self):
        """Get config file path (works for both dev and executable)"""
        if getattr(sys, 'frozen', False):
            # Running as executable
            base_path = Path(sys.executable).parent
        else:
            # Running as script
            base_path = Path(__file__).parent
        
        return base_path / "config.json"
    
    def load_config(self):
        """Load configuration from file or environment"""
        default_config = {
            "host": "0.0.0.0",
            "port": 8000,
            "model_path": "models/qwen-14b.gguf",
            "n_ctx": 4096,
            "n_gpu_layers": -1,  # -1 = use all GPU layers, 0 = CPU only
            "n_threads": 4,
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "verbose": False
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                file_config = json.load(f)
                default_config.update(file_config)
        
        self.data = default_config
    
    def get(self, key, default=None):
        return self.data.get(key, default)

config = Config()

# Global model instance
llm_model = None
executor = ThreadPoolExecutor(max_workers=1)

def load_model():
    """Load the Qwen model"""
    global llm_model
    
    if Llama is None:
        raise RuntimeError("llama-cpp-python not installed. Run: pip install llama-cpp-python")
    
    model_path = config.get("model_path")
    if not Path(model_path).exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}\n"
            f"Please download a GGUF model or check your config.json path."
        )
    
    print(f"Loading model from {model_path}...")
    llm_model = Llama(
        model_path=model_path,
        n_ctx=config.get("n_ctx", 4096),
        n_gpu_layers=config.get("n_gpu_layers", -1),
        n_threads=config.get("n_threads", 4),
        verbose=config.get("verbose", False)
    )
    print("Model loaded successfully!")

# Initialize FastAPI app
app = FastAPI(
    title="LLM Server - Local Models",
    description="HTTP API for local LLM model completions (supports Qwen, Llama, etc.)",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
    except Exception as e:
        print(f"Failed to load model: {e}")
        print("Server will start but /v1/chat/completions will not work.")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatMessage(BaseModel):
    role: str
    content: str

class CompletionRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    repeat_penalty: Optional[float] = None
    stream: Optional[bool] = False

class CompletionResponse(BaseModel):
    content: str
    model: str = "qwen-14b"
    usage: Optional[Dict[str, Any]] = None

def format_chat_prompt(messages: List[ChatMessage], model_path: str = "") -> str:
    """Format messages for appropriate chat template based on model"""
    
    # Detect model type from path
    model_name = model_path.lower()
    
    # Llama 3.1 format
    if "llama" in model_name or "sha256" in model_name:
        formatted = ""
        for msg in messages:
            if msg.role == "system":
                formatted += f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{msg.content}<|eot_id|>"
            elif msg.role == "user":
                formatted += f"<|start_header_id|>user<|end_header_id|>\n\n{msg.content}<|eot_id|>"
            elif msg.role == "assistant":
                formatted += f"<|start_header_id|>assistant<|end_header_id|>\n\n{msg.content}<|eot_id|>"
        formatted += "<|start_header_id|>assistant<|end_header_id|>\n\n"
        return formatted
    
    # Qwen format (default)
    else:
        formatted = ""
        for msg in messages:
            if msg.role == "system":
                formatted += f"<|im_start|>system\n{msg.content}<|im_end|>\n"
            elif msg.role == "user":
                formatted += f"<|im_start|>user\n{msg.content}<|im_end|>\n"
            elif msg.role == "assistant":
                formatted += f"<|im_start|>assistant\n{msg.content}<|im_end|>\n"
        formatted += "<|im_start|>assistant\n"
        return formatted

async def local_completion(request: CompletionRequest) -> CompletionResponse:
    """Handle local model completion"""
    if llm_model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Check server logs for errors."
        )
    
    try:
        # Format the prompt based on model type
        prompt = format_chat_prompt(request.messages, config.get("model_path", ""))
        
        # Run inference in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            executor,
            lambda: llm_model(
                prompt,
                max_tokens=request.max_tokens or config.get("max_tokens", 2000),
                temperature=request.temperature or config.get("temperature", 0.7),
                top_p=request.top_p or config.get("top_p", 0.95),
                top_k=request.top_k or config.get("top_k", 40),
                repeat_penalty=request.repeat_penalty or config.get("repeat_penalty", 1.1),
                stop=["<|im_end|>", "<|endoftext|>"],
                echo=False
            )
        )
        
        content = response["choices"][0]["text"].strip()
        
        return CompletionResponse(
            content=content,
            model="qwen-14b",
            usage={
                "prompt_tokens": response["usage"]["prompt_tokens"],
                "completion_tokens": response["usage"]["completion_tokens"],
                "total_tokens": response["usage"]["total_tokens"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference error: {str(e)}")

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "version": "1.0.0",
        "model": "qwen-14b",
        "model_loaded": llm_model is not None,
        "model_path": config.get("model_path")
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/v1/chat/completions", response_model=CompletionResponse)
async def chat_completion(request: CompletionRequest):
    """
    Create a chat completion using the local Qwen 14B model
    """
    return await local_completion(request)

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return config.data

@app.get("/model/info")
async def model_info():
    """Get model information"""
    if llm_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model": "qwen-14b",
        "context_length": config.get("n_ctx", 4096),
        "gpu_layers": config.get("n_gpu_layers", -1),
        "loaded": True
    }

# Main entry point
def main():
    """Main entry point for the server"""
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 8000)
    
    print(f"Starting LLM Server on {host}:{port}")
    print(f"API Documentation available at http://{host}:{port}/docs")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()
