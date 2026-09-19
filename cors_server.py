#!/usr/bin/env python
"""CORS-enabled HTTP server for Dify DSL import"""
import http.server
import socketserver
import os

PORT = 8003
DIRECTORY = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace"

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

with socketserver.TCPServer(("", PORT), CORSHandler) as httpd:
    print(f"Serving CORS-enabled files at http://localhost:{PORT}")
    httpd.serve_forever()
