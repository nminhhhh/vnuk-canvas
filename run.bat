@echo off
title FastAPI Server - Antigravity
cd /d "%~dp0"

echo [1/2] Kiem tra moi truong Python...
if exist ".venv\Scripts\python.exe" (
    echo [2/2] Khoi dong server bang .venv...
    ".venv\Scripts\python.exe" run.py
) else (
    echo [2/2] Khoi dong server bang Python he thong...
    python run.py
)
pause
