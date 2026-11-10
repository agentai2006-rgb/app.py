import os
import time
from threading import Thread
from flask import Flask, render_template_string
from flask_socketio import SocketIO
import MetaTrader5 as mt5

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Professional ChainX Style Financial & MT5 Trading Dashboard UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChainX - Pro MT5 Trading Dashboard</title>
    <style>
        :root {
            --bg-main: #0b0f17;
            --sidebar-bg: #0f1523;
            --card-bg: #131b2e;
            --card-border: rgba(255, 255, 255, 0.06);
            --accent-purple: #8b5cf6;
            --accent-cyan: #38bdf8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Inter, sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-main); display: flex; height: 100vh; overflow: hidden; }

        /* Sidebar */
        aside {
            width: 260px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--card-border);
            display: flex;
            flex-direction: column;
            padding: 24px 20px;
            gap: 30px;
        }

        .logo-area { display: flex; align-items: center; gap: 12px; font-size: 1.3rem; font-weight: 800; }
        .logo-icon { width: 14px; height: 14px; background: var(--accent-purple); box-shadow: 0 0 12px var(--accent-purple); transform: rotate(45deg); }

        .nav-links { display: flex; flex-direction: column; gap: 8px; }
        .nav-item {
            padding: 12px 14px;
            border-radius: 10px;
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }
        .nav-item:hover, .nav-item.active { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }

        /* Main Wrapper */
        .main-wrapper { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }

        /* Top Bar */
        .topbar {
            height: 70px;
            border-bottom: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
            background: var(--bg-main);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .market-ticker { display: flex; gap: 20px; font-size: 0.85rem; color: var(--text-muted); }
        .ticker-item span { color: var(--accent-green); font-weight: 600; }

        .top-right { display: flex; align-items: center; gap: 16px; }
        .balance-pill { background: var(--card-bg); border: 1px solid var(--card-border); padding: 8px 16px; border-radius: 20px; font-weight: 700; color: var(--accent-cyan); }

        /* Dashboard Content */
        .content { padding: 30px; display: flex; flex-direction: column; gap: 24px; }

        .dashboard-header { display: flex; justify-content: space-between; align-items: center; }
        .dashboard-title h1 { font-size: 1.6rem; font-weight: 800; margin-bottom: 4px; }
        .dashboard-title p { color: var(--text-muted); font-size: 0.9rem; }

        .btn-action { background: var(--accent-purple); color: #fff; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 700; cursor: pointer; transition: filter 0.2s; }
        .btn-action:hover { filter: brightness(1.15); }

        /* Grid Metrics */
        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        @media (max-width: 1024px) { .metrics-grid { grid-template-columns: 1fr; } }

        .card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
        .card-title { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); }
        .card-value { font-size: 2.2rem; font-weight: 800; }
        .card-sub { font-size: 0.85rem; color: var(--accent-green); font-weight: 600; }

        /* Bottom Section: Table & AI Box */
        .bottom-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
        @media (max-width: 1024px) { .bottom-grid { grid-template-columns: 1fr; } }

        table { width: 100%; border-collapse: collapse; text-align: left; margin-top: 10px; }
        th { color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; padding: 10px 12px; border-bottom: 1px solid var(--card-border); }
        td { padding: 14px 12px; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 0.9rem; }

        .pnl-pos { color: var(--accent-green); font-weight: 700; }
        .pnl-neg { color: var(--accent-red); font-weight: 700; }

        /* AI Robo Advisor Card */
        .ai-card {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(56, 189, 248, 0.1));
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
        }
        .ai-icon { font-size: 2.5rem; margin-bottom: 10px; }
        .ai-card h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }
        .ai-card p { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 20px; }
    </style>
</head>
<body>

    <!-- Sidebar -->
    <aside>
        <div class="logo-area">
            <div class="logo-icon"></div>
            ChainX
        </div>
        <div class="nav-links">
            <a class="nav-item active">Dashboard</a>
            <a class="nav-item">Market Summary</a>
            <a class="nav-item">Portfolio</a>
            <a class="nav-item">Analytics</a>
            <a class="nav-item">Wallet</a>
            <a class="nav-item">Settings</a>
        </div>
    </aside>

    <!-- Main Content Area -->
    <div class="main-wrapper">
        <!-- Top Navigation -->
        <header class="topbar">
            <div class="market-ticker">
                <div class="ticker-item">AAPL <span>+0.45%</span></div>
                <div class="ticker-item">TSLA <span>+1.20%</span></div>
                <div class="ticker-item">NVDA <span>+2.10%</span></div>
            </div>
            <div class="top-right">
                <div class="balance-pill" id="top-balance">Balance: $0.00</div>
            </div>
        </header>

        <!-- Dashboard Body -->
        <div class="content">
            <div class="dashboard-header">
                <div class="dashboard-title">
                    <h1>Dashboard</h1>
                    <p>Live update from your MetaTrader 5 terminal ecosystem.</p>
                </div>
                <button class="btn-action">Execute Asset</button>
            </div>

            <!-- Top Metric Cards -->
            <div class="metrics-grid">
                <div class="card">
                    <div class="card-title">Account Equity</div>
                    <div class="card-value" id="card-equity">$0.00</div>
                    <div class="card-sub" id="card-profit-sub">Floating P&L: $0.00</div>
                </div>
                <div class="card">
                    <div class="card-title">Total Balance</div>
                    <div class="card-value" id="card-balance">$0.00</div>
                    <div class="card-sub" style="color: var(--accent-cyan);">MT5 Connected Live</div>
                </div>
            </div>

            <!-- Positions Table & AI Box -->
            <div class="bottom-grid">
                <div class="card">
                    <div class="card-title">Active Market Positions</div>
                    <table>
                        <thead>
                            <tr>
                                <th>Ticket</th>
                                <th>Symbol</th>
                                <th>Type</th>
                                <th>Volume</th>
                                <th>Profit ($)</th>
                            </tr>
                        </thead>
                        <tbody id="positions-tbody">
                            <tr><td colspan="5" style="color: var(--text-muted); text-align:center; padding: 20px;">Synchronizing MT5 positions...</td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- AI Robo Advisor -->
                <div class="ai-card">
                    <div>
                        <div class="ai-icon">🤖</div>
                        <h3>Invest Smarter with Our AI-Robo Advisor!</h3>
                        <p>Get automated risk monitoring, live market insights, and optimized stop-loss calculations.</p>
                    </div>
                    <button class="btn-action">Activate AI Agent</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Socket.IO Client -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();

        socket.on('update_data', (data) => {
            // Update Top Balance & Cards
            document.getElementById('top-balance').textContent = `Balance: $${data.balance.toFixed(2)}`;
            document.getElementById('card-balance').textContent = `$${data.balance.toFixed(2)}`;
            document.getElementById('card-equity').textContent = `$${data.equity.toFixed(2)}`;
            
            const subProfit = document.getElementById('card-profit-sub');
            subProfit.textContent = `Floating P&L: ${data.profit >= 0 ? '+' : ''}$${data.profit.toFixed(2)}`;
            subProfit.className = `card-sub ${data.profit >= 0 ? 'pnl-pos' : 'pnl-neg'}`;

            // Update Positions Table
            const tbody = document.getElementById('positions-tbody');
            tbody.innerHTML = '';

            if (data.positions.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" style="color: var(--text-muted); text-align:center; padding: 20px;">No open positions in MT5.</td></tr>`;
                return;
            }

            data.positions.forEach(pos => {
                const row = document.createElement('tr');
                const isPos = pos.profit >= 0;
                row.innerHTML = `
                    <td>${pos.ticket}</td>
                    <td><strong>${pos.symbol}</strong></td>
                    <td><span style="color: ${pos.type === 0 ? 'var(--accent-green)' : 'var(--accent-red)'}; font-weight:700;">${pos.type === 0 ? 'BUY' : 'SELL'}</span></td>
                    <td>${pos.volume}</td>
                    <td class="${isPos ? 'pnl-pos' : 'pnl-neg'}">${isPos ? '+' : ''}$${pos.profit.toFixed(2)}</td>
                `;
                tbody.appendChild(row);
            });
        });
    </script>
</body>
</html>
"""

def background_mt5_thread():
    """Background loop fetching data from local MT5 terminal"""
    while True:
        if not mt5.initialize():
            time.sleep(2)
            continue

        account_info = mt5.account_info()
        if account_info is not None:
            balance = account_info.balance
            equity = account_info.equity
            profit = account_info.profit

            positions = mt5.positions_get()
            positions_list = []
            if positions is not None:
                for pos in positions:
                    positions_list.append({
                        "ticket": pos.ticket,
                        "symbol": pos.symbol,
                        "type": pos.type,
                        "volume": pos.volume,
                        "profit": pos.profit
                    })

            # Broadcast live metrics to website
            socketio.emit('update_data', {
                "balance": balance,
                "equity": equity,
                "profit": profit,
                "positions": positions_list
            })

        time.sleep(1)

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    t = Thread(target=background_mt5_thread, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
