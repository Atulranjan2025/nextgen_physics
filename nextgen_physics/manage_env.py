"""
🔄 Smart Auto Environment Detector for Django
Author: Atul Ranjan (NextGen Physics)
--------------------------------------
Automatically detects if the app is running on Render (production)
or locally, and loads the correct environment file accordingly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import socket

BASE_DIR = Path(__file__).resolve().parent.parent

def detect_environment():
    hostname = socket.gethostname().lower()
    render_env = os.getenv("RENDER", None)
    domain_env = os.getenv("RENDER_EXTERNAL_HOSTNAME", "")

    # 🚀 If Render or cloud hostname is found
    if "render" in hostname or render_env or ".onrender.com" in domain_env:
        mode = "production"
    else:
        mode = "local"

    return mode

def setup_environment():
    mode = detect_environment()

    # Set MODE env globally
    os.environ["MODE"] = mode

    # Load .env files
    if mode == "production":
        load_dotenv(BASE_DIR / ".env.production")
        print("🚀 Auto-detected: PRODUCTION (Render)")
    else:
        load_dotenv(BASE_DIR / ".env.local")
        print("💻 Auto-detected: LOCAL (Development)")

    # Debug info
    print(f"✅ Environment Loaded: {mode}")
    print(f"✅ Hostname: {socket.gethostname()}")
    print(f"✅ Base Directory: {BASE_DIR}")

# Run this immediately on import
setup_environment()
