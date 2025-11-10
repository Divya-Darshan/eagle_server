async function load() {
    const leaderboardDiv = document.getElementById("leaderboard");
    
    try {
        // Use localhost for local development, fallback to production URL
        const baseUrl = window.location.origin;
        let res = await fetch(`${baseUrl}/leaderboard`, {
            cache: "no-store"
        });
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        let data = await res.json();

        if (data.length === 0) {
            leaderboardDiv.innerHTML = `
                <div class="empty-state">
                    <h2>🏆</h2>
                    <p>No scores yet! Be the first to play!</p>
                </div>
            `;
            return;
        }

        // Get top 3 unique scores for medal assignment
        const topScores = [];
        const seenScores = new Set();
        for (let i = 0; i < data.length && topScores.length < 3; i++) {
            const score = parseFloat(data[i].score);
            if (!seenScores.has(score)) {
                topScores.push(score);
                seenScores.add(score);
            }
        }

        let html = '';
        data.forEach((row, i) => {
            const rank = i + 1;
            const score = parseFloat(row.score);
            let medal = '';
            let rankClass = '';
            let scoreClass = '';
            
            // Check if this player's score matches any of the top 3 unique scores
            if (topScores.length > 0 && score === topScores[0]) {
                // Gold medal - tied for 1st place
                medal = '🥇';
                rankClass = 'top1';
                scoreClass = 'top1';
            } else if (topScores.length > 1 && score === topScores[1]) {
                // Silver medal - tied for 2nd place
                medal = '🥈';
                rankClass = 'top2';
                scoreClass = 'top2';
            } else if (topScores.length > 2 && score === topScores[2]) {
                // Bronze medal - tied for 3rd place
                medal = '🥉';
                rankClass = 'top3';
                scoreClass = 'top3';
            }

            html += `
                <div class="leaderboard-item" style="animation-delay: ${i * 0.1}s">
                    <div class="rank ${rankClass}">${rank}</div>
                    ${medal ? `<div class="medal">${medal}</div>` : ''}
                    <div class="player-info">
                        <div class="username">${escapeHtml(row.username)}</div>
                    </div>
                    <div class="score ${scoreClass}">${formatScore(row.score)}</div>
                </div>
            `;
        });

        leaderboardDiv.innerHTML = html;
    } catch (e) {
        console.error("Error loading leaderboard:", e);
        leaderboardDiv.innerHTML = `
            <div class="empty-state">
                <h2>⚠️</h2>
                <p>Unable to load leaderboard. Please check your connection.</p>
            </div>
        `;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatScore(score) {
    return parseFloat(score).toLocaleString('en-US', {
        maximumFractionDigits: 0
    });
}

// Auto refresh every 3 seconds
setInterval(load, 3000);

// Initial load
load();
