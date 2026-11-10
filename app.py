import os
import time
from threading import Thread
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import MetaTrader5 as mt5

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Professional Dark Theme Dashboard with WebSocket Live Updates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live MT5 AI Trading Dashboard</title>
    <style>
        :root {
            --bg-color: #030712;
            --card-bg: rgba(15, 23, 42, 0.75);
            --accent-cyan: #38bdf8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: rgba(56, 189, 248, 0.2);
            --glow-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Inter, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; padding: 20px; }

        .container { max-width: 1280px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }

        header {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 18px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--glow-shadow);
        }

        .logo { font-size: 1.4rem; font-weight: 800; letter-spacing: 2px; display: flex; align-items: center; gap: 12px; }
        .logo-icon { width: 12px; height: 12px; background: var(--accent-cyan); box-shadow: 0 0 12px var(--accent-cyan); transform: rotate(45deg); }

        .status-badge {
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(34, 197, 94, 0.4);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
        }

        .stat-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 24px;
            box-shadow: var(--glow-shadow);
        }

        .stat-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); margin-bottom: 8px; }
        .stat-value { font-size: 2.2rem; font-weight: 800; }

        /* Panel Layout */
        .panel {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
        }

        .panel-header { font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--accent-cyan); margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }

        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { background: rgba(30, 41, 59, 0.5); color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; padding: 14px; border-bottom: 1px solid var(--border-color); }
        td { padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.9rem; }

        .pnl-pos { color: var(--accent-green); font-weight: 700; }
        .pnl-neg { color: var(--accent-red); font-weight: 700; }
        .empty-text { text-align: center; padding: 30px; color: var(--text-muted); }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <div class="logo">
                <div class="logo-icon"></div>
                MT5 LIVE TRADING TERMINAL
            </div>
            <div class="status-badge" id="connection-status">MT5 CONNECTED</div>
        </header>

        <!-- Live Account Metrics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Account Balance</div>
                <div class="stat-value" id="acc-balance">$0.00</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Account Equity</div>
                <div class="stat-value" id="acc-equity" style="color: var(--accent-cyan);">$0.00</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Floating Profit / Loss</div>
                <div class="stat-value" id="acc-profit">$0.00</div>
            </div>
        </div>

        <!-- Live Positions Panel -->
        <div class="panel">
            <div class="panel-header">Active Market Positions</div>
            <table>
                <thead>
                    <tr>
                        <th>Ticket</th>
                        <th>Symbol</th>
                        <th>Type</th>
                        <th>Volume</th>
                        <th>Open Price</th>
                        <th>Profit ($)</th>
                    </tr>
                </thead>
                <tbody id="positions-table">
                    <tr><td colspan="6" class="empty-text">Fetching live data from MT5 terminal...</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Socket.IO Client -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();

        socket.on('update_data', (data) => {
            // Update Account Info
            document.getElementById('acc-balance').textContent = `$${data.balance.toFixed(2)}`;
            document.getElementById('acc-equity').textContent = `$${data.equity.toFixed(2)}`;
            
            const profitEl = document.getElementById('acc-profit');
            profitEl.textContent = `${data.profit >= 0 ? '+' : ''}$${data.profit.toFixed(2)}`;
            profitEl.className = `stat-value ${data.profit >= 0 ? 'pnl-pos' : 'pnl-neg'}`;

            // Update Positions Table
            const tbody = document.getElementById('positions-table');
            tbody.innerHTML = '';

            if (data.positions.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="empty-text">No active positions open.</td></tr>`;
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
                    <td>${pos.price_open}</td>
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
    """Background thread to poll MT5 terminal and push live data via WebSocket"""
    while True:
        if not mt5.initialize():
            print("MT5 initialization failed, retrying...")
            time.sleep(2)
            continue

        # Get Account Info
        account_info = mt5.account_info()
        if account_info is not None:
            balance = account_info.balance
            equity = account_info.equity
            profit = account_info.profit

            # Get Open Positions
            positions = mt5.positions_get()
            positions_list = []
            if positions is not None:
                for pos in positions:
                    positions_list.append({
                        "ticket": pos.ticket,
                        "symbol": pos.symbol,
                        "type": pos.type, # 0 = Buy, 1 = Sell
                        "volume": pos.volume,
                        "price_open": pos.price_open,
                        "profit": pos.profit
                    })

            # Broadcast data to all connected web clients
            socketio.emit('update_data', {
                "balance": balance,
                "equity": equity,
                "profit": profit,
                "positions": positions_list
            })

        time.sleep(1) # Refresh rate every 1 second

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    # Start MT5 background poller thread
    t = Thread(target=background_mt5_thread, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
                        
