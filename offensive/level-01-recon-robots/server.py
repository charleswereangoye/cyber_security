import http.server
import socketserver
import signal
import sys

PORT = 8080

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def handle_exit(sig, frame):
    print("\n[!] Shutting down Level 1 server...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":
    with ReusableTCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"[+] Level 1 Offensive Lab Server running on port {PORT}...")
        httpd.serve_forever()
