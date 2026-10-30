import http.server
import socketserver
import signal
import sys
import urllib.parse
import json

PORT = 8080
ADMIN_TOKEN = "master_chef_token_2026"

class CulinaryLabHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean logging format
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Landing Page
        if path == "" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Culinary Hub Portal</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #1e293b; border: 1px solid #334155; padding: 2.5rem; border-radius: 12px; text-align: center; max-width: 480px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; margin-top: 0; }
        p { color: #94a3b8; line-height: 1.6; }
        .status { display: inline-block; background: #0284c7; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <span class="status">MAINTENANCE MODE</span>
        <h1>Culinary Hub & Kitchen API</h1>
        <p>Our cooking recipe database and administrative control dashboard are currently undergoing scheduled maintenance.</p>
        <p style="font-size: 0.85rem; color: #64748b;">All automated scans and unauthorized access attempts are logged.</p>
    </div>
</body>
</html>""")
            return

        # 2. robots.txt
        if path == "/robots.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"""# robots.txt - Culinary Hub Security Policy
User-agent: *
Disallow: /admin/
Disallow: /internal/

# Dev memo: Staging configurations and backup files must not be indexed by bots.
""")
            return

        # 3. Leaked backup file: config.bak
        if path == "/config.bak":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            config_data = {
                "system": "Culinary Hub API v2.1",
                "environment": "staging-to-prod",
                "database": "sqlite:///data/kitchen.db",
                "dev_notes": "TODO: remove this config backup before Friday launch! Dev emergency token for admin panel is: master_chef_token_2026",
                "admin_auth_token": "master_chef_token_2026"
            }
            self.wfile.write(json.dumps(config_data, indent=2).encode())
            return

        # 4. Leaked developer note: secret.txt
        if path in ("/secret.txt", "/notes.txt"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"""[INTERNAL DEV MEMO]
To: Kitchen Portal Web Team
From: Lead Developer
Subject: Temporary Admin Token

We implemented authentication on /admin/.
If you need to test the chef dashboard, append:
  ?token=master_chef_token_2026
or pass header:
  X-Admin-Token: master_chef_token_2026

Remember to delete this memo and config.bak!
""")
            return

        # 5. Protected Admin Panel
        if path == "/admin":
            token_provided = query.get("token", [None])[0]
            header_token = self.headers.get("X-Admin-Token")

            if token_provided == ADMIN_TOKEN or header_token == ADMIN_TOKEN:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Master Chef Admin Panel</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; border: 1px solid #10b981; padding: 2.5rem; border-radius: 12px; max-width: 550px; width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        .badge { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
        h1 { margin-top: 15px; color: #34d399; font-size: 1.6rem; }
        p { color: #cbd5e1; line-height: 1.6; }
        .flag-box { background: #022c22; border: 2px dashed #10b981; padding: 1.2rem; border-radius: 8px; margin: 20px 0; font-family: monospace; font-size: 1.05rem; color: #6ee7b7; word-break: break-all; }
        .footer { font-size: 0.8rem; color: #64748b; text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">Access Granted</span>
        <h1>Executive Chef Control Panel</h1>
        <p>Authenticated successfully via leaked developer token. You bypassed the access restriction!</p>
        
        <div class="flag-box">
            Flag{fuzzing_extensions_revealed_the_keys_to_the_kitchen}
        </div>

        <p style="font-size: 0.9rem; color: #94a3b8;">
            Offensive Lesson: Always check for backup extensions (.bak, .old, .txt, .json). Developers often leave sensitive keys right in web root!
        </p>

        <div class="footer">Offensive Lab &bull; Level 2 Complete</div>
    </div>
</body>
</html>""")
                return
            else:
                self.send_response(403)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>403 Forbidden</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #1e293b; border: 1px solid #ef4444; padding: 2.5rem; border-radius: 12px; text-align: center; max-width: 480px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h1 { color: #ef4444; margin-top: 0; }
        p { color: #94a3b8; }
        .code { background: #0f172a; padding: 8px 12px; border-radius: 6px; font-family: monospace; color: #f87171; display: inline-block; margin-top: 10px; border: 1px solid #7f1d1d; }
    </style>
</head>
<body>
    <div class="box">
        <h1>403 Forbidden</h1>
        <p>Administrative authentication is required. Direct access is denied.</p>
        <div class="code">Error: Missing or invalid token parameter (?token=...)</div>
    </div>
</body>
</html>""")
                return

        # 6. Default 404 Not Found
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def handle_exit(sig, frame):
    print("\n[!] Shutting down Level 2 server...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":
    with ReusableTCPServer(("", PORT), CulinaryLabHandler) as httpd:
        print(f"[+] Level 2 Culinary Lab Server running on port {PORT}...")
        httpd.serve_forever()
