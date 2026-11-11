"""Tiny standard-library HTTP mock for the Nginx routing exercise."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

NAME = os.getenv('SERVICE_NAME', 'unknown')
PORT = int(os.getenv('SERVICE_PORT', '8081'))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = json.dumps({'service': NAME, 'path': self.path, 'status': 'ok'}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    print(f'Started {NAME} at {PORT}', flush=True)
    HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
