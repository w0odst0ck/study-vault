#!/usr/bin/env python3
"""本地运行复习小站"""
import http.server
import os
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
SITE = Path(__file__).resolve().parent.parent / "site"

os.chdir(SITE)
print(f"📚 study-vault 本地服务 → http://localhost:{PORT}")
print(f"   按 Ctrl+C 停止")
http.server.HTTPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
