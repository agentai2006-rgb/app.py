import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Complete English Trading Journal UI with HTML, CSS & JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Trading Journal</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(21, 30, 48, 0.7);
            --accent-cyan: #38bdf8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --text-main: #f3f4f6;
            --text-muted: #94a3b8;
            --border-color: rgba(255, 255, 255, 0.08);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Inter, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 30px 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: 1px;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo span {
            color: var(--accent-cyan);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }

        .stat-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
        }

        .main-content {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 24px;
        }

        @media (max-width: 900px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }

        .form-panel, .table-panel {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }

        .form-panel {
            height: fit-content;
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 16px;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 14px;
        }

        .form-group label {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .form-group input, .form-group select, .form-group textarea {
            background: rgba(11, 15, 25, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 12px;
            color: var(--text-main);
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s ease;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--accent-cyan);
        }

        .btn-submit {
            width: 100%;
            background: var(--accent-cyan);
            color: #0b0f19;
            font-weight: 700;
            padding: 12px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: opacity 0.2s ease;
            margin-top: 8px;
        }

        .btn-submit:hover {
            opacity: 0.9;
        }

        .table-panel {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background: rgba(11, 15, 25, 0.5);
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
            padding: 12px 14px;
            border-bottom: 1px solid var(--border-color);
        }

        td {
            padding: 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            vertical-align: middle;
        }

        .badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge-buy {
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
        }

        .badge-sell {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
        }

        .pnl-positive {
            color: var(--accent-green);
            font-weight: 700;
        }

        .pnl-negative {
            color: var(--accent-red);
            font-weight: 700;
        }

        .btn-delete {
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1rem;
            transition: color 0.2s ease;
        }

        .btn-delete:hover {
            color: var(--accent-red);
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <div class="logo">
                <span>⚡</span> TRADING JOURNAL
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Total Trades</div>
                <div class="stat-value" id="stat-total">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Win Rate</div>
                <div class="stat-value" id="stat-winrate" style="color: var(--accent-cyan);">0%</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Net P&L ($)</div>
                <div class="stat-value" id="stat-pnl">$0.00</div>
            </div>
        </div>

        <div class="main-content">
            <div class="form-panel">
                <div class="section-title">Log New Trade</div>
                <form id="trade-form">
                    <div class="form-group">
                        <label>Date</label>
                        <input type="date" id="trade-date" required>
                    </div>

                    <div class="form-group">
                        <label>Asset / Pair</label>
                        <input type="text" id="trade-pair" placeholder="e.g. EUR/USD or BTC/USD" required>
                    </div>

                    <div class="form-group">
                        <label>Direction</label>
                        <select id="trade-direction">
                            <option value="BUY">BUY / LONG</option>
                            <option value="SELL">SELL / SHORT</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Lot Size / Position</label>
                        <input type="number" step="0.01" id="trade-size" placeholder="1.00" required>
                    </div>

                    <div class="form-group">
                        <label>Profit / Loss ($)</label>
                        <input type="number" step="0.01" id="trade-pnl" placeholder="e.g. 150 or -50" required>
                    </div>

                    <div class="form-group">
                        <label>Strategy / Notes</label>
                        <textarea id="trade-notes" rows="3" placeholder="Setup strategy, emotions, or key takeaways..."></textarea>
                    </div>

                    <button type="submit" class="btn-submit">Save Trade</button>
                </form>
            </div>

            <div class="table-panel">
                <div class="section-title">Trade History</div>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Pair</th>
                            <th>Type</th>
                            <th>Size</th>
                            <th>P&L ($)</th>
                            <th>Notes</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="trade-list"></tbody>
                </table>
                <div id="empty-msg" class="empty-state">No trades logged yet. Start by filling out the form!</div>
            </div>
        </div>
    </div>

    <script>
        let trades = JSON.parse(localStorage.getItem('trading_journal_data')) || [];

        const form = document.getElementById('trade-form');
        const tradeList = document.getElementById('trade-list');
        const emptyMsg = document.getElementById('empty-msg');

        const statTotal = document.getElementById('stat-total');
        const statWinrate = document.getElementById('stat-winrate');
        const statPnl = document.getElementById('stat-pnl');

        document.getElementById('trade-date').valueAsDate = new Date();

        function saveAndRender() {
            localStorage.setItem('trading_journal_data', JSON.stringify(trades));
            render();
        }

        function render() {
            tradeList.innerHTML = '';
            
            if (trades.length === 0) {
                emptyMsg.style.display = 'block';
            } else {
                emptyMsg.style.display = 'none';
            }

            let totalPnl = 0;
            let wins = 0;

            trades.forEach((trade, index) => {
                totalPnl += parseFloat(trade.pnl);
                if (parseFloat(trade.pnl) > 0) wins++;

                const row = document.createElement('tr');
                const isPositive = parseFloat(trade.pnl) >= 0;

                row.innerHTML = `
                    <td>${trade.date}</td>
                    <td><strong>${trade.pair.toUpperCase()}</strong></td>
                    <td><span class="badge ${trade.direction === 'BUY' ? 'badge-buy' : 'badge-sell'}">${trade.direction}</span></td>
                    <td>${trade.size}</td>
                    <td class="${isPositive ? 'pnl-positive' : 'pnl-negative'}">${isPositive ? '+' : ''}$${parseFloat(trade.pnl).toFixed(2)}</td>
                    <td style="color: var(--text-muted); font-size: 0.85rem;">${trade.notes || '-'}</td>
                    <td><button class="btn-delete" onclick="deleteTrade(${index})">✕</button></td>
                `;
                tradeList.appendChild(row);
            });

            statTotal.textContent = trades.length;
            const winRate = trades.length > 0 ? ((wins / trades.length) * 100).toFixed(1) : 0;
            statWinrate.textContent = `${winRate}%`;
            statPnl.textContent = `${totalPnl >= 0 ? '+' : ''}$${totalPnl.toFixed(2)}`;
            statPnl.className = `stat-value ${totalPnl >= 0 ? 'pnl-positive' : 'pnl-negative'}`;
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const newTrade = {
                date: document.getElementById('trade-date').value,
                pair: document.getElementById('trade-pair').value,
                direction: document.getElementById('trade-direction').value,
                size: document.getElementById('trade-size').value,
                pnl: document.getElementById('trade-pnl').value,
                notes: document.getElementById('trade-notes').value
            };

            trades.unshift(newTrade);
            saveAndRender();

            document.getElementById('trade-pair').value = '';
            document.getElementById('trade-size').value = '';
            document.getElementById('trade-pnl').value = '';
            document.getElementById('trade-notes').value = '';
        });

        function deleteTrade(index) {
            trades.splice(index, 1);
            saveAndRender();
        }

        render();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
