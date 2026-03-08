# 🦅 Eagle Server - Leaderboard Project

A blazing-fast Python HTTP server for managing game leaderboards. Track scores, compete with friends, and dominate the rankings!

## ✨ Features

- 📊 Real-time leaderboard display with auto-refresh
- 🚀 Simple REST API for score submissions
- 💾 Persistent JSON-based storage
- 🌐 Accessible from any device on your network
- 🏆 Automatic highest-score tracking per player

## 📋 Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## 🚀 Quick Start

### Option 1: Development (Recommended for testing)

```bash

python server.py
```

Then open your browser to **`http://localhost:8000`** 🎮

The leaderboard will display and automatically refresh every 3 seconds!

### Option 3: Custom Port

```bash
PORT=3000 python server.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` or `/index.html` | Leaderboard webpage |
| `GET` | `/leaderboard` | JSON leaderboard data (sorted by score) |
| `POST` | `/submit_score` | Submit a new score |

**Submit Score Example:**
```json
{
  "username": "PlayerName",
  "score": 100
}
```

## 📁 Project Structure

```
eagle_score/
├── server.py           # Main server logic
├── index.html          # Leaderboard UI
├── leaderboard.json    # Score database (auto-generated)
└── requirements.txt    # Python dependencies
```

## 💡 How It Works

1. **Submit scores** via the POST endpoint
2. **Highest score wins** - duplicate entries update only if the new score is higher
3. **Auto-refresh** - the web UI updates every 3 seconds
4. **Network accessible** - access from any device on your local network

## ⚙️ Configuration

- **Server binds to:** `0.0.0.0` (all network interfaces)
- **Data storage:** `leaderboard.json` (created automatically)
- **Default port:** `8000`

## 📝 Notes

- Leaderboard data persists between server restarts
- Each player's highest score is automatically preserved 

