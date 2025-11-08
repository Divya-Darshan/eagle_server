import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

LEADERBOARD_FILE = "leaderboard.json"
HTML_FILE = "index.html"

# Create leaderboard file if missing
try:
    open(LEADERBOARD_FILE, "x").write("[]")
except:
    pass


class LeaderboardServer(BaseHTTPRequestHandler):

    # ---------------------------------------------------
    # ✅ Serve index.html for "/" or "/index.html"
    # ---------------------------------------------------
    def serve_html(self, filename):
        if not os.path.exists(filename):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - File Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    # ---------------------------------------------------
    # ✅ Handle GET requests
    # ---------------------------------------------------
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_html(HTML_FILE)
            return

        if self.path == "/leaderboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            leaderboard = json.load(open(LEADERBOARD_FILE))
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

            self.wfile.write(json.dumps(leaderboard).encode())
            return

        # Fallback 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 - Not Found")

    # ---------------------------------------------------
    # ✅ Handle POST requests from Godot
    # ---------------------------------------------------
    def do_POST(self):
        if self.path == "/submit_score":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)

            username = data.get("username", "Unknown")
            score = data.get("score", 0)

            leaderboard = json.load(open(LEADERBOARD_FILE))
            leaderboard.append({"username": username, "score": score})
            json.dump(leaderboard, open(LEADERBOARD_FILE, "w"), indent=2)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Score Saved")
            return

        # Fallback 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 - Not Found")


server = HTTPServer(("127.0.0.1", 8000), LeaderboardServer)
print("✅ Server running at http://127.0.0.1:8000")
server.serve_forever()
