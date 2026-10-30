import http.server
import socketserver
import signal
import sys
import urllib.parse

PORT = 8080

RECIPES = {
    "1": {
        "title": "Classic French Omelette",
        "category": "Breakfast & Brunch",
        "visibility": "Public",
        "author": "Sous Chef Antoine",
        "description": "A velvety, pale yellow folded omelette cooked gently in clarified butter, garnished with fresh chives.",
        "ingredients": ["3 large farm eggs", "2 tbsp unsalted butter", "1 tbsp minced fresh chives", "Flaky sea salt", "White pepper"],
        "secret": False
    },
    "2": {
        "title": "Tuscan Garlic Pasta",
        "category": "Main Entrees",
        "visibility": "Public",
        "author": "Chef Marco",
        "description": "Al dente fettuccine tossed in extra virgin olive oil, toasted garlic chips, crushed red pepper, and aged pecorino.",
        "ingredients": ["250g fettuccine", "6 cloves garlic (thinly sliced)", "1/3 cup cold-pressed olive oil", "1 tsp chili flakes", "Fresh parsley", "Pecorino Romano"],
        "secret": False
    },
    "3": {
        "title": "Executive Chef Confidential: Grand Reserve Truffle Glaze",
        "category": "Proprietary Sauce Vault",
        "visibility": "Internal Only / Confidential",
        "author": "Executive Chef Sterling",
        "description": "Proprietary slow-reduction demi-glace infused with winter black truffles and 25-year aged balsamic. Kept strictly confidential.",
        "ingredients": ["1 liter veal reduction", "50g minced Périgord black truffle", "100ml vintage port", "Aged balsamic", "Unsalted cultured butter"],
        "secret": True,
        "flag": "Flag{idor_parameter_tampering_revealed_the_secret_recipe}"
    }
}

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Culinary Hub - Recipe Management Portal</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 2rem; }
        .container { max-width: 800px; margin: 0 auto; }
        header { border-bottom: 1px solid #334155; padding-bottom: 1.5rem; margin-bottom: 2rem; }
        h1 { margin: 0 0 0.5rem 0; font-size: 1.75rem; color: #38bdf8; }
        p.subtitle { margin: 0; color: #94a3b8; font-size: 0.95rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; }
        .card h2 { margin: 0 0 0.5rem 0; font-size: 1.25rem; color: #f1f5f9; }
        .card p { color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin: 0 0 1rem 0; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 0.75rem; }
        .badge-public { background: #065f46; color: #6ee7b7; }
        .badge-secret { background: #831843; color: #fbcfe8; border: 1px solid #db2777; }
        .btn { display: inline-block; text-align: center; background: #0284c7; color: white; text-decoration: none; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.85rem; font-weight: 500; }
        .btn:hover { background: #0369a1; }
        .flag-box { background: #022c22; border: 2px dashed #10b981; border-radius: 6px; padding: 1rem; font-family: monospace; font-size: 1rem; color: #6ee7b7; margin: 1.5rem 0; word-break: break-all; }
        .nav-back { display: inline-block; margin-bottom: 1.5rem; color: #38bdf8; text-decoration: none; font-size: 0.9rem; }
        ul { margin: 0 0 1.5rem 0; padding-left: 1.25rem; color: #cbd5e1; font-size: 0.9rem; }
        li { margin-bottom: 0.35rem; }
        footer { margin-top: 3rem; text-align: center; font-size: 0.8rem; color: #64748b; border-top: 1px solid #334155; padding-top: 1.5rem; }
    </style>
</head>
<body>
<div class="container">
"""

HTML_FOOTER = """
    <footer>Culinary Hub &bull; Level 3: Broken Access Control Lab</footer>
</div>
</body>
</html>
"""

class RecipeHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        query = urllib.parse.parse_qs(parsed.query)

        if path == "" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            body = HTML_HEADER + """
    <header>
        <h1>Culinary Hub Recipe Management</h1>
        <p class="subtitle">Public Recipe Portal &mdash; Internal staff and proprietary recipes are restricted.</p>
    </header>
    <div class="grid">
        <div class="card">
            <div>
                <span class="badge badge-public">Public Recipe #1</span>
                <h2>Classic French Omelette</h2>
                <p>A velvety folded omelette cooked gently in clarified butter with fresh garden herbs.</p>
            </div>
            <a href="/recipe?id=1" class="btn">View Recipe Details &rarr;</a>
        </div>
        <div class="card">
            <div>
                <span class="badge badge-public">Public Recipe #2</span>
                <h2>Tuscan Garlic Pasta</h2>
                <p>Al dente fettuccine tossed in extra virgin olive oil, toasted garlic, and aged pecorino.</p>
            </div>
            <a href="/recipe?id=2" class="btn">View Recipe Details &rarr;</a>
        </div>
    </div>
""" + HTML_FOOTER
            self.wfile.write(body.encode('utf-8'))
            return

        if path == "/recipe":
            recipe_id = query.get("id", [None])[0]

            if not recipe_id or recipe_id not in RECIPES:
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                error_body = HTML_HEADER + """
    <a href="/" class="nav-back">&larr; Back to Catalog</a>
    <h1>404 &mdash; Recipe Not Found</h1>
    <p class="subtitle">No recipe exists for the requested record identifier.</p>
""" + HTML_FOOTER
                self.wfile.write(error_body.encode('utf-8'))
                return

            item = RECIPES[recipe_id]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            if item["secret"]:
                badge = '<span class="badge badge-secret">RESTRICTED &bull; CONFIDENTIAL</span>'
                flag_section = f"""
    <div class="flag-box">
        <strong>VULNERABILITY CONFIRMED: Insecure Direct Object Reference (IDOR)</strong><br><br>
        {item['flag']}
    </div>
    <p style="color: #94a3b8; font-size: 0.85rem;">
        Developer Lesson: The backend trusted client-supplied parameter <code>id={recipe_id}</code> without checking if the current user has permission to access internal confidential records.
    </p>
"""
            else:
                badge = '<span class="badge badge-public">Public Entry</span>'
                flag_section = ""

            ingredients_list = "".join(f"<li>{ing}</li>" for ing in item["ingredients"])

            body = HTML_HEADER + f"""
    <a href="/" class="nav-back">&larr; Back to Catalog</a>
    <header>
        {badge}
        <h1>{item['title']}</h1>
        <p class="subtitle">Category: {item['category']} &bull; Author: {item['author']}</p>
    </header>
    
    <p>{item['description']}</p>
    
    <h3>Key Ingredients</h3>
    <ul>
        {ingredients_list}
    </ul>
    
    {flag_section}
""" + HTML_FOOTER
            self.wfile.write(body.encode('utf-8'))
            return

        if path == "/robots.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"User-agent: *\nDisallow: /admin/\n")
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def handle_exit(sig, frame):
    print("\n[!] Shutting down Level 3 server...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":
    with ReusableTCPServer(("", PORT), RecipeHandler) as httpd:
        print(f"[+] Level 3 Recipe Portal running on port {PORT}...")
        httpd.serve_forever()
