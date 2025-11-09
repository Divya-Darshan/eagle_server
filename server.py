import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

LEADERBOARD_FILE = "leaderboard.json"
HTML_FILE = "index.html"


# ✅ Create file if missing
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        f.write("[]")


# ✅ Safe JSON load
def load_json():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("[ERROR] load_json failed:", e)
        return []


# ✅ Safe JSON save
def save_json(data):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("[ERROR] save_json failed:", e)


class LeaderboardServer(BaseHTTPRequestHandler):

    # ✅ Small helper: send JSON response
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow browser
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # ✅ Small helper: send HTML file
    def send_html(self, filename):
        if not os.path.exists(filename):
            self.send_error(404, "HTML file not found")
            return

        try:
            with open(filename, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            print("[ERROR] send_html failed:", e)
            self.send_error(500, "Internal Server Error")

    # ----------------------------------------------------
    # ✅ Handle GET
    # ----------------------------------------------------
    def do_GET(self):
        try:
            # Serve HTML page
            if self.path in ("/", "/index.html"):
                self.send_html(HTML_FILE)
                return

            # Serve leaderboard JSON
            if self.path == "/leaderboard":
                data = load_json()
                data = sorted(data, key=lambda x: x["score"], reverse=True)
                self.send_json(data)
                return

            # Not found
            self.send_error(404, "Not Found")

        except Exception as e:
            print("[ERROR] GET failed:", e)
            self.send_error(500, "Internal Server Error")

    # ----------------------------------------------------
    # ✅ Handle POST (Godot)
    # ----------------------------------------------------
    def do_POST(self):
        if self.path == "/submit_score":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            username = data.get("username", "Unknown")
            score = data.get("score", 0)

            leaderboard = load_json()

            # ✅ Update or add score
            found = False
            for entry in leaderboard:
                if entry["username"] == username:
                    entry["score"] = max(entry["score"], score)
                    found = True
                    break

            if not found:
                leaderboard.append({"username": username, "score": score})

            save_json(leaderboard)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Score Saved")
            return

        # If wrong path
        self.send_error(404, "Invalid POST endpoint")

# ✅ Start server safely
try:
    server = HTTPServer(("127.0.0.1", 8000), LeaderboardServer)
    print("✅ Server running at http://127.0.0.1:8000")
    server.serve_forever()

except KeyboardInterrupt:
    print("\n✅ Server stopped.")
except Exception as e:
    print("❌ Server failed to start:", e)
