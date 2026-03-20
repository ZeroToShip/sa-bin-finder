#!/usr/bin/env python3
import http.server, os, sys

PORT = 4500
DIR  = "/Users/agnesmuthoni/Claude-Cowork/Active Project Folder/salvation-army-bins"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

with http.server.HTTPServer(("", PORT), Handler) as httpd:
    print(f"Serving {DIR} on port {PORT}")
    httpd.serve_forever()
