import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Exact ChainX Dashboard UI Replica
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChainX - Financial Dashboard</title>
    <style>
        :root {
            --bg-main: #0b0f17;
            --sidebar-bg: #0f1523;
            --card-bg: #131b2e;
            --card-border: rgba(255, 255, 255, 0.06);
            --accent-purple: #8b5cf6;
            --accent-cyan: #38bdf8;
            --accent-green: #22c55e;
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
            gap: 20px;
            justify-content: space-between;
        }

        .sidebar-top { display: flex; flex-direction: column; gap: 30px; }
        .logo-area { display: flex; align-items: center; gap: 12px; font-size: 1.3rem; font-weight: 800; }
        .logo-icon { width: 14px; height: 14px; background: var(--accent-purple); box-shadow: 0 0 12px var(--accent-purple); transform: rotate(45deg); }

        .nav-section { display: flex; flex-direction: column; gap: 6px; }
        .nav-label { font-size: 0.7rem; text-transform: uppercase; color: #475569; letter-spacing: 1px; margin-bottom: 6px; padding-left: 10px; }
        .nav-item {
            padding: 10px 14px;
            border-radius: 10px;
            color: var(--text-muted);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .nav-item:hover, .nav-item.active { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }

        .sidebar-bottom-card {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(15, 21, 35, 0.8));
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .sidebar-bottom-card h4 { font-size: 0.9rem; font-weight: 700; }
        .sidebar-bottom-card p { font-size: 0.75rem; color: var(--text-muted); }
        .upgrade-btn { background: var(--accent-purple); color: white; border: none; padding: 8px; border-radius: 8px; font-weight: 700; font-size: 0.75rem; cursor: pointer; }

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

        .market-ticker { display: flex; gap: 20px; font-size: 0.8rem; color: var(--text-muted); align-items: center; }
        .ticker-item { display: flex; align-items: center; gap: 6px; }
        .ticker-item span { color: var(--accent-green); font-weight: 600; }

        .top-right { display: flex; align-items: center; gap: 16px; }
        .balance-pill { background: var(--card-bg); border: 1px solid var(--card-border); padding: 8px 16px; border-radius: 20px; font-weight: 700; color: var(--accent-cyan); font-size: 0.85rem; display: flex; align-items: center; gap: 8px; }
        .pill-btns { display: flex; gap: 6px; }
        .pill-btn { width: 28px; height: 28px; background: var(--accent-purple); border: none; border-radius: 50%; color: white; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; }

        /* Dashboard Content */
        .content { padding: 30px; display: flex; flex-direction: column; gap: 24px; }

        .dashboard-header { display: flex; justify-content: space-between; align-items: center; }
        .dashboard-title h1 { font-size: 1.5rem; font-weight: 800; margin-bottom: 4px; }
        .dashboard-title p { color: var(--text-muted); font-size: 0.85rem; }

        .header-actions { display: flex; gap: 12px; align-items: center; }
        .btn-action { background: var(--accent-purple); color: #fff; border: none; padding: 10px 18px; border-radius: 10px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: filter 0.2s; }
        .btn-action:hover { filter: brightness(1.15); }
        .btn-outline { background: var(--card-bg); border: 1px solid var(--card-border); color: var(--text-main); padding: 10px 16px; border-radius: 10px; font-weight: 600; font-size: 0.85rem; cursor: pointer; }

        /* Grid Metrics */
        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        @media (max-width: 1024px) { .metrics-grid { grid-template-columns: 1fr; } }

        .card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
        .card-top-row { display: flex; justify-content: space-between; align-items: center; }
        .card-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); }
        .card-value { font-size: 2rem; font-weight: 800; }
        
        .progress-bar-container { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
        .progress-bg { width: 100%; height: 8px; background: #0b0f17; border-radius: 4px; overflow: hidden; display: flex; }
        .prog-1 { width: 65%; background: var(--accent-purple); }
        .prog-2 { width: 25%; background: var(--accent-cyan); }
        .prog-3 { width: 10%; background: var(--accent-green); }

        .distribution-legend { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
        .legend-item { display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted); }
        .legend-item span strong { color: var(--text-main); }

        /* Chart mock area */
        .chart-visual { height: 160px; display: flex; align-items: flex-end; justify-content: space-between; padding-top: 20px; border-bottom: 1px solid var(--card-border); }
        .chart-line-mock { width: 100%; height: 100px; background: linear-gradient(to top, rgba(139,92,246,0.05), rgba(139,92,246,0.3)); border-top: 2px solid var(--accent-purple); position: relative; border-radius: 4px; }

        /* Bottom Section */
        .bottom-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
        @media (max-width: 1024px) { .bottom-grid { grid-template-columns: 1fr; } }

        .bars-container { display: flex; justify-content: space-between; align-items: flex-end; height: 140px; padding-top: 20px; }
        .bar-col { display: flex; flex-direction: column; align-items: center; gap: 8px; flex: 1; }
        .bar-fill { width: 24px; background: var(--accent-purple); border-radius: 6px 6px 0 0; }
        .bar-label { font-size: 0.7rem; color: var(--text-muted); }

        /* AI Robo Advisor Card */
        .ai-card {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(56, 189, 248, 0.05));
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
        }
        .ai-icon { font-size: 2.2rem; margin-bottom: 8px; }
        .ai-card h3 { font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
        .ai-card p { color: var(--text-muted); font-size: 0.8rem; margin-bottom: 16px; line-height: 1.4; }
    </style>
</head>
<body>

    <!-- Sidebar -->
    <aside>
        <div class="sidebar-top">
            <div class="logo-area">
                <div class="logo-icon"></div>
                Chainx
            </div>
            <div class="nav-section">
                <div class="nav-label">Main Menu</div>
                <a class="nav-item active">📊 Dashboard</a>
                <a class="nav-item">📈 Market Summary</a>
                <a class="nav-item">💼 Portfolio</a>
                <a class="nav-item">📉 Analytics</a>
                <a class="nav-item">👛 Wallet</a>
                <a class="nav-item">🌐 Community</a>
            </div>
            <div class="nav-section">
                <div class="nav-label">Preferences</div>
                <a class="nav-item">⚙️ Settings</a>
                <a class="nav-item">💬 Help & Support</a>
            </div>
        </div>

        <div class="sidebar-bottom-card">
            <h4>Upgrade</h4>
            <p>Unlock all chainx features & tools</p>
            <button class="upgrade-btn">Go Pro</button>
        </div>
    </aside>

    <!-- Main Content Area -->
    <div class="main-wrapper">
        <!-- Top Navigation Bar -->
        <header class="topbar">
            <div class="market-ticker">
                <div class="ticker-item">🟢 The market is open</div>
                <div class="ticker-item">AAPL <span>+0.45%</span></div>
                <div class="ticker-item">TSLA <span>+1.20%</span></div>
                <div class="ticker-item">NVDA <span>+2.10%</span></div>
            </div>
            <div class="top-right">
                <div class="balance-pill">
                    Balance: $25,760.98
                    <div class="pill-btns">
                        <button class="pill-btn">+</button>
                    </div>
                </div>
            </div>
        </header>

        <!-- Dashboard Content Body -->
        <div class="content">
            <div class="dashboard-header">
                <div class="dashboard-title">
                    <h1>Dashboard</h1>
                    <p>Happy to see you again. Get update of your asset today!</p>
                </div>
                <div class="header-actions">
                    <button class="btn-outline">All Time ▾</button>
                    <button class="btn-action">Buy Asset</button>
                </div>
            </div>

            <!-- Top Metric Cards (Total Assets & Investments) -->
            <div class="metrics-grid">
                <div class="card">
                    <div class="card-title">Total Assets</div>
                    <div class="card-value">$325,980.65</div>
                    <div style="color: var(--accent-green); font-size: 0.85rem; font-weight: 600;">+12% +$39,117.67 in this year</div>
                    
                    <div class="progress-bar-container">
                        <div class="card-title" style="margin-bottom: 2px;">Distribution</div>
                        <div class="progress-bg">
                            <div class="prog-1"></div>
                            <div class="prog-2"></div>
                            <div class="prog-3"></div>
                        </div>
                        <div class="distribution-legend">
                            <div class="legend-item"><span>🟣 Stocks (65%)</span> <strong>$211,887.42</strong></div>
                            <div class="legend-item"><span>🔵 Bonds (25%)</span> <strong>$81,495.16</strong></div>
                            <div class="legend-item"><span>🟢 Mutual Funds (10%)</span> <strong>$32,598.06</strong></div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-title">Total Investments</div>
                    <div class="card-value">$270,560.20</div>
                    <div style="color: var(--accent-green); font-size: 0.85rem; font-weight: 600;">+20% +$54,112.04 in this year</div>
                    
                    <!-- Line Chart Mock -->
                    <div style="margin-top: 15px;">
                        <div class="chart-line-mock"></div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--text-muted); margin-top: 6px;">
                            <span>2018</span><span>2019</span><span>2020</span><span>2021</span><span>2022</span><span>2023</span><span>2024</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Section (Total Profits & AI Robo Advisor) -->
            <div class="bottom-grid">
                <div class="card">
                    <div class="card-title">Total Profits</div>
                    <div class="card-value" style="font-size: 1.6rem;">$55,420.45</div>
                    <div style="color: var(--accent-green); font-size: 0.8rem; font-weight: 600;">+7% +$9,879.43 in this year</div>

                    <!-- Bar Chart Breakdown -->
                    <div class="bars-container">
                        <div class="bar-col"><div class="bar-fill" style="height: 40%;"></div><span class="bar-label">2018</span></div>
                        <div class="bar-col"><div class="bar-fill" style="height: 60%;"></div><span class="bar-label">2019</span></div>
                        <div class="bar-col"><div class="bar-fill" style="height: 45%;"></div><span class="bar-label">2020</span></div>
                        <div class="bar-col"><div class="bar-fill" style="height: 75%;"></div><span class="bar-label">2021</span></div>
                        <div class="bar-col"><div class="bar-fill" style="height: 90%;"></div><span class="bar-label">2022</span></div>
                        <div class="bar-col"><div class="bar-fill" style="height: 65%;"></div><span class="bar-label">2023</span></div>
                        <div class="bar-col"><div class="bar-fill" style="height: 100%;"></div><span class="bar-label">2024</span></div>
                    </div>
                </div>

                <!-- AI Robo Advisor -->
                <div class="ai-card">
                    <div>
                        <div class="ai-icon">🤖</div>
                        <h3>Invest Smarter with Our AI-Robo Advisor!</h3>
                        <p>Get automated management, real-time insights, and personalized advice.</p>
                    </div>
                    <button class="btn-action" style="width: 100%;">Try Now</button>
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
    
