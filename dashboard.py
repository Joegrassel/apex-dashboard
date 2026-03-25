from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>APEX Dashboard</title>
    <meta http-equiv="refresh" content="5">

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: #0b0f14;
            color: #fff;
        }

        .container {
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #00eaff;
            margin-bottom: 30px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .card {
            background: #121821;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            text-align: center;
        }

        .card h2 {
            margin: 0;
            font-size: 16px;
            color: #888;
        }

        .card p {
            font-size: 24px;
            margin-top: 10px;
            color: #00ff9f;
        }

        canvas {
            margin-top: 40px;
            background: #121821;
            border-radius: 12px;
            padding: 20px;
        }
    </style>
</head>

<body>

<div class="container">

<h1>APEX TRADING DASHBOARD</h1>

<div class="grid">

    <div class="card">
        <h2>Balance</h2>
        <p>${{balance}}</p>
    </div>

    <div class="card">
        <h2>Trades</h2>
        <p>{{trades}}</p>
    </div>

    <div class="card">
        <h2>Win Rate</h2>
        <p>{{win_rate}}%</p>
    </div>

    <div class="card">
        <h2>Wins</h2>
        <p>{{wins}}</p>
    </div>

    <div class="card">
        <h2>Losses</h2>
        <p>{{losses}}</p>
    </div>

</div>

<canvas id="chart"></canvas>

</div>

<script>
    const dataPoints = {{history}};

    const ctx = document.getElementById('chart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataPoints.map((_, i) => i + 1),
            datasets: [{
                label: 'Balance',
                data: dataPoints,
                borderColor: '#00ff9f',
                tension: 0.2
            }]
        }
    });
</script>

</body>
</html>
"""

# =========================
# LOAD STATS + HISTORY
# =========================
def load_stats():
    if os.path.exists("stats.json"):
        return json.load(open("stats.json"))
    return {"balance": 0, "wins": 0, "losses": 0, "trades": 0}

def load_history():
    if os.path.exists("history.json"):
        return json.load(open("history.json"))
    return []

# =========================
# ROUTE
# =========================
@app.route("/")
def home():
    stats = load_stats()
    history = load_history()

    trades = stats["trades"]
    win_rate = (stats["wins"]/trades*100) if trades else 0

    return render_template_string(
        HTML,
        balance=round(stats["balance"], 2),
        trades=trades,
        wins=stats["wins"],
        losses=stats["losses"],
        win_rate=round(win_rate, 2),
        history=history
    )

# =========================
# RUN
# =========================
if __name__ == "__main__":
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)