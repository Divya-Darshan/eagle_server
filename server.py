import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

LEADERBOARD_FILE = "leaderboard.json"
HTML_FILE = "index.html"

# ✅ Create leaderboard file if missing
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        f.write("[]")

# ✅ Safe JSON loader
def load_json():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# ✅ Safe JSON writer
def save_json(data):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass


class LeaderboardServer(BaseHTTPRequestHandler):

    # ✅ Helper: send JSON response
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # ✅ Helper: send HTML
    def send_html(self, filename):
        if not os.path.exists(filename):
            self.send_error(404, "HTML not found")
            return

        try:
            with open(filename, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except:
            self.send_error(500, "Internal Server Error")

    # ✅ Helper: send static files (CSS, JS)
    def send_static(self, filename, content_type):
        if not os.path.exists(filename):
            self.send_error(404, "File not found")
            return

        try:
            with open(filename, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except:
            self.send_error(500, "Internal Server Error")

    # --------------------------------------------------------
    # ✅ GET
    # --------------------------------------------------------
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_html(HTML_FILE)
            return

        if self.path == "/leaderboard":
            data = load_json()

            # ✅ FIX: Convert all scores to float
            for entry in data:
                try:
                    entry["score"] = float(entry["score"])
                except:
                    entry["score"] = 0

            # ✅ Sort after conversion
            data = sorted(data, key=lambda x: x["score"], reverse=True)

            self.send_json(data)
            return

        # Serve CSS and JS files
        if self.path == "/styles.css":
            self.send_static("styles.css", "text/css")
            return

        if self.path == "/script.js":
            self.send_static("script.js", "application/javascript")
            return

        self.send_error(404, "Not Found")

    # --------------------------------------------------------
    # ✅ POST (Godot Game Sends Score Here)
    # --------------------------------------------------------
    def do_POST(self):
        if self.path != "/submit_score":
            self.send_error(404, "Invalid POST endpoint")
            return

        length = int(self.headers.get("Content-Length", 0))
        incoming = json.loads(self.rfile.read(length))

        username = incoming.get("username", "Unknown")

        # ✅ FIX: Always convert incoming string score → float
        try:
            score = float(incoming.get("score", 0))
        except:
            score = 0

        leaderboard = load_json()

        # ✅ Update / insert
        found = False
        for entry in leaderboard:
            if entry["username"] == username:
                entry["score"] = max(float(entry["score"]), score)
                found = True
                break

        if not found:
            leaderboard.append({"username": username, "score": score})

        save_json(leaderboard)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"Score Saved")


# --------------------------------------------------------
# ✅ RENDER DEPLOY FIX — dynamic port + public host
# --------------------------------------------------------
PORT = int(os.environ.get("PORT", 8000))

print(f"✅ Starting server on port {PORT}...")
server = HTTPServer(("0.0.0.0", PORT), LeaderboardServer)
print(f"✅ Server running at http://0.0.0.0:{PORT}")

server.serve_forever()
