# Eagle Server - Leaderboard Project

A simple Python HTTP server for managing a game leaderboard.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## How to Run

### Option 1: Run with Python's built-in server (Recommended for development)

1. **Install dependencies** (optional - only needed if using gunicorn):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python server.py
   ```

3. **Access the application**:
   - Open your browser and go to: `http://localhost:8000`
   - The leaderboard will be displayed and auto-refresh every 3 seconds

### Option 2: Run with Gunicorn (Recommended for production)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with gunicorn**:
   ```bash
   gunicorn server:LeaderboardServer --bind 0.0.0.0:8000
   ```
   
   Note: You may need to modify `server.py` slightly for gunicorn compatibility.

### Option 3: Run on a custom port

Set the `PORT` environment variable:
```bash
PORT=3000 python server.py
```

## API Endpoints

- `GET /` or `GET /index.html` - Serves the leaderboard HTML page
- `GET /leaderboard` - Returns JSON data of all leaderboard entries (sorted by score)
- `POST /submit_score` - Submit a new score
  - Body: `{"username": "PlayerName", "score": 100}`

## Files

- `server.py` - Main server application
- `index.html` - Frontend leaderboard display
- `leaderboard.json` - Data file storing leaderboard entries (auto-created if missing)
- `requirements.txt` - Python dependencies

## Notes

- The server runs on `0.0.0.0` (all interfaces) by default, making it accessible from other devices on your network
- The leaderboard data is stored in `leaderboard.json` in the same directory
- If a user submits multiple scores, only their highest score is kept
