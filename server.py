import http.server
import socketserver

# This turns the folder the script is in into a live web server
with socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler) as httpd:
    print("Server is live on port 8080...")
    httpd.serve_forever()