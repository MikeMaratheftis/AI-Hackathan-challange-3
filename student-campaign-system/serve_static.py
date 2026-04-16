#!/usr/bin/env python3
"""
Simple HTTP server to serve the interactive wireframes
Run: python serve_static.py
Then open: http://localhost:8000
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
STATIC_DIR = Path(__file__).parent / 'static'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(STATIC_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {STATIC_DIR}")
        print(f"\n✨ Interactive Wireframes:")
        print(f"   - Student Portal: Application Form, Status, Progress Reports")
        print(f"   - Admin Dashboard: Overview, Applications, Configuration")
        print(f"\n💡 Features:")
        print(f"   - Real-time character counting")
        print(f"   - Form validation")
        print(f"   - Tab navigation")
        print(f"   - Application filtering")
        print(f"   - Score visualization")
        print(f"   - Configuration management")
        print(f"\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
