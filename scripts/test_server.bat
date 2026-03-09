@echo off
REM Test the server
echo Testing Qwen LLM Server...
echo.

cd /d "%~dp0.."
python scripts\test_server.py

pause
