import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ChainX Style Pure Frontend UI (No MT5 Engine yet)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChainX - Pro Dashboard UI</title>
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

        /* Bottom Section: Analytics & AI Box */
        .bottom-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
        @media (max-width: 1024px) { .bottom-grid { grid-template-columns: 1fr; } }

        .chart-placeholder {
            height: 180px;
            background: rgba(15, 21, 35, 0.5);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            border: 1px dashed rgba(255, 255, 255, 0.1);
        }

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
                <div class="balance-pill">Balance: $25,760.98</div>
            </div>
        </header>

        <!-- Dashboard Body -->
        <div class="content">
            <div class="dashboard-header">
                <div class="dashboard-title">
                    <h1>Dashboard</h1>
                    <p>Happy to see you again. Get update of your asset today!</p>
                </div>
                <button class="btn-action">Buy Asset</button>
            </div>

            <!-- Top Metric Cards -->
            <div class="metrics-grid">
                <div class="card">
                    <div class="card-title">Total Assets</div>
                    <div class="card-value">$325,980.65</div>
                    <div class="card-sub">+12% +$39,117.67 in this year</div>
                </div>
                <div class="card">
                    <div class="card-title">Total Investments</div>
                    <div class="card-value">$270,560.20</div>
                    <div class="card-sub">+20% +$54,112.04 in this year</div>
                </div>
            </div>

            <!-- Chart & AI Box Section -->
            <div class="bottom-grid">
                <div class="card">
                    <div class="card-title">Portfolio Performance Overview</div>
                    <div class="chart-placeholder">
                        📊 [Interactive Chart Placeholder - Ready for Engine Data]
                    </div>
                </div>

                <!-- AI Robo Advisor -->
                <div class="ai-card">
                    <div>
                        <div class="ai-icon">🤖</div>
                        <h3>Invest Smarter with Our AI-Robo Advisor!</h3>
                        <p>Get automated management, real-time insights, and personalized advice.</p>
                    </div>
                    <button class="btn-action">Try Now</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
