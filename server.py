"""
JARVIS Web Server & API Gateway
Serves the Stark Holographic HUD and processes voice/text commands.
"""

import http.server
import socketserver
import json
import os
import sys
import mimetypes
from pathlib import Path
from jarvis_brain import JarvisBrain

PORT = 7860
brain = JarvisBrain()
PUBLIC_DIR = Path(__file__).parent / "public"

class JarvisRequestHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API Status Endpoint
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            status_data = {
                "status": "online",
                "version": "2.0.0",
                "system": "JARVIS Stark Industries Protocol Active"
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
            return

        # System info endpoint
        if self.path == "/api/system":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = brain.system.get_system_status()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        # Serve Static Files
        req_path = self.path.split('?')[0].lstrip('/')
        if req_path == '' or req_path == '/':
            req_path = 'index.html'

        file_path = PUBLIC_DIR / req_path
        if file_path.is_file():
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(file_path)
            self.send_header('Content-Type', mime_type or 'application/octet-stream')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path == "/api/command":
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_body)
                cmd = data.get("command", "")
                print(f"[JARVIS RECEIVED]: {cmd}")
                
                # Process with JARVIS Agent Brain
                result = brain.process_command(cmd)
                print(f"[JARVIS ACTION]: {result.get('message', '')}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e), "message": "Command processing failed."}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server(port=PORT):
    # Ensure port is reusable
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), JarvisRequestHandler) as httpd:
        print(f"\n=======================================================")
        print(f"⚡ J.A.R.V.I.S. AI SYSTEM IS ONLINE & OPERATIONAL ⚡")
        print(f"📡 Access JARVIS HUD at: http://localhost:{port}")
        print(f"=======================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down JARVIS...")
            httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
