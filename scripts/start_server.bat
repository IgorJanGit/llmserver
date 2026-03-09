@echo off
REM Quick server starter for Windows
REM Double-click this file to start the server

echo =====================================
echo   Qwen LLM Server - Starting...
echo =====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Change to project root
cd /d "%~dp0.."

REM Check if model exists
if not exist "models\qwen-14b.gguf" (
    echo WARNING: Model file not found!
    echo Please download Qwen 14B model to: models\qwen-14b.gguf
    echo.
    echo Download from:
    echo https://huggingface.co/Qwen/Qwen-14B-Chat-GGUF
    echo.
    pause
    exit /b 1
)

echo Starting server...
echo.
echo Server will be available at:
echo   http://localhost:8000
echo   http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
