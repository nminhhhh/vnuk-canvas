"""Entrypoint script to start the FastAPI server with dynamic PORT and UTF-8 encoding support."""
import os
from pathlib import Path
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Guarantee project root is in working directory and sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")

    print("\n" + "=" * 60)
    print(f"[*] Antigravity FastAPI + Gemini 3.8 Flash Online on port {port}!")
    print(f"[*] Web Dashboard:  http://{host}:{port}")
    print(f"[*] Swagger Docs:   http://{host}:{port}/api/v1/docs")
    print(f"[*] Health Status:  http://{host}:{port}/api/v1/health")
    print("=" * 60 + "\n")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
