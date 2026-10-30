import http.server
import socketserver
import signal
import sys
import urllib.parse

PORT = 8080

VALID_USERS = {
    "admin": "password",
    "headchef": "kitchen2026"
}

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Culinary Hub - Staff Portal</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 2rem; display: flex; justify-content: center; align-items: center; min-height: 85vh; }
        .box { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 2rem; max-width: 440px; width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.4); }
        h1 { margin: 0 0 0.5rem 0; font-size: 1.5rem; color: #38bdf8; }
        p.subtitle { margin: 0 0 1.5rem 0; color: #94a3b8; font-size: 0.9rem; }
        .form-group { margin-bottom: 1.25rem; }
        label { display: block; margin-bottom: 0.4rem; font-size: 0.85rem; color: #cbd5e1; font-weight: 500; }
        input[type="text"], input[type="password"] { width: 100%; box-sizing: border-box; background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 0.65rem 0.75rem; color: #f8fafc; font-size: 0.95rem; }
        input:focus { outline: none; border-color: #38bdf8; }
        button { width: 100%; background: #0284c7; color: white; border: none; padding: 0.75rem; border-radius: 6px; font-weight: 600; font-size: 0.95rem; cursor: pointer; margin-top: 0.5rem; }
        button:hover { background: #0369a1; }
        .alert { background: #450a0a; border: 1px solid #dc2626; color: #fecaca; padding: 0.75rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1.25rem; }
        .notice { background: #0c4a6e; border: 1px solid #0284c7; color: #bae6fd; padding: 0.75rem; border-radius: 6px; font-size: 0.8rem; margin-top: 1.5rem; line-height: 1.4; }
        .flag-box { background: #022c22; border: 2px dashed #10b981; border-radius: 6px; padding: 1.25rem; font-family: monospace; font-size: 0.95rem; color: #6ee7b7; margin: 1.5rem 0; word-break: break-all; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 0.75rem; background: #065f46; color: #6ee7b7; }
        footer { margin-top: 2rem; text-align: center; font-size: 0.8rem; color: #64748b; }
    </style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

def render_login(error_msg=None):
    error_html = f'<div class="alert">{error_msg}</div>' if error_msg else ''
    return HTML_HEADER + f"""
<div class="box">
    <h1>Staff Authentication</h1>
    <p class="subtitle">Culinary Hub Internal Employee & Kitchen Portal</p>
    
    {error_html}
    
    <form action="/login" method="POST">
        <div class="form-group">
            <label for="username">Staff Username</label>
            <input type="text" id="username" name="username" required autocomplete="off" placeholder="e.g. admin">
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required placeholder="••••••••">
        </div>
        <button type="submit">Authenticate &rarr;</button>
    </form>
    
    <div class="notice">
        <strong>Security Policy Notice:</strong> Newly provisioned staff accounts (including standard <code>admin</code>) are automatically initialized with default temporary credentials. Please update your password immediately after first sign-in.
    </div>
    
    <footer>Culinary Hub &bull; Level 4 Practice Target</footer>
</div>
""" + HTML_FOOTER

def render_dashboard(username):
    return HTML_HEADER + f"""
<div class="box" style="max-width: 550px;">
    <span class="badge">Session Authenticated</span>
    <h1>Welcome, {username.capitalize()}</h1>
    <p class="subtitle">Access granted to Culinary Hub Staff & System Control.</p>
    
    <div class="flag-box">
        <strong>AUTHENTICATION AUDIT SUCCESSFUL</strong><br><br>
        Flag{{username_enumeration_and_weak_credentials_compromised}}
    </div>
    
    <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">
        Full-Stack Lesson: The application suffered from two common flaws:<br>
        1. <strong>Username Enumeration</strong>: Verbose error messages revealed whether a username existed in the database.<br>
        2. <strong>Default Credentials</strong>: The admin account used a standard default password (<code>password</code>).
    </p>
    
    <p><a href="/login" style="color: #38bdf8; font-size: 0.9rem; text-decoration: none;">&larr; Log out of portal</a></p>
    <footer>Culinary Hub &bull; Level 4 Practice Target</footer>
</div>
""" + HTML_FOOTER

class AuthHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        if path in ("", "/login", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(render_login().encode('utf-8'))
            return

        if path == "/robots.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"User-agent: *\nDisallow: /login\nDisallow: /admin/\n")
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        if path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
            params = urllib.parse.parse_qs(post_data)

            username = params.get("username", [""])[0].strip()
            password = params.get("password", [""])[0].strip()

            # Vulnerability 1: Username Enumeration via verbose error messages
            if username not in VALID_USERS:
                self.send_response(401)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(render_login(f"Authentication Error: User account '{username}' was not found in the staff directory.").encode('utf-8'))
                return

            # Check password
            if password != VALID_USERS[username]:
                self.send_response(401)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(render_login(f"Authentication Error: Incorrect password supplied for account '{username}'.").encode('utf-8'))
                return

            # Success
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(render_dashboard(username).encode('utf-8'))
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def handle_exit(sig, frame):
    print("\n[!] Shutting down Level 4 server...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":
    with ReusableTCPServer(("", PORT), AuthHandler) as httpd:
        print(f"[+] Level 4 Auth Target running on port {PORT}...")
        httpd.serve_forever()
