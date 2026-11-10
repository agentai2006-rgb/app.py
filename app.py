import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Sci-Fi Glassmorphism UI with 3D Holographic Chart Animation Background
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D AI Trading Journal & Analytics</title>
    <style>
        :root {
            --bg-color: #030712;
            --card-bg: rgba(15, 23, 42, 0.65);
            --accent-cyan: #38bdf8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: rgba(56, 189, 248, 0.2);
            --glow-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
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
            overflow-x: hidden;
            min-height: 100vh;
        }

        /* 3D Canvas Background */
        #canvas-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1;
            pointer-events: none;
        }

        /* Glassmorphism Wrapper */
        .container {
            position: relative;
            z-index: 10;
            max-width: 1280px;
            margin: 0 auto;
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        header {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            box-shadow: var(--glow-shadow);
            border-radius: 16px;
            padding: 18px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: var(--text-main);
        }

        .logo-icon {
            width: 12px;
            height: 12px;
            background: var(--accent-cyan);
            box-shadow: 0 0 12px var(--accent-cyan);
            transform: rotate(45deg);
        }

        .badge-live {
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(34, 197, 94, 0.4);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        /* Stats Section */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
        }

        .stat-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 22px;
            box-shadow: var(--glow-shadow);
            transition: transform 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
        }

        .stat-title {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 800;
        }

        /* Layout Grid */
        .main-content {
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 24px;
        }

        @media (max-width: 960px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }

        .panel {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: var(--glow-shadow);
        }

        .panel-header {
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent-cyan);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 16px;
        }

        .form-group label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
        }

        .form-group input, .form-group select, .form-group textarea {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 12px;
            color: var(--text-main);
            font-size: 0.9rem;
            outline: none;
            transition: all 0.2s ease;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
        }

        .btn-submit {
            width: 100%;
            background: var(--accent-cyan);
            color: #030712;
            font-weight: 800;
            padding: 14px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
            transition: all 0.2s ease;
            margin-top: 10px;
        }

        .btn-submit:hover {
            filter: brightness(1.15);
            transform: scale(1.01);
        }

        /* History Table */
        .table-responsive {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th {
            background: rgba(30, 41, 59, 0.5);
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 14px;
            border-bottom: 1px solid var(--border-color);
        }

        td {
            padding: 16px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.9rem;
        }

        .badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 800;
        }

        .badge-buy {
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(34, 197, 94, 0.3);
        }

        .badge-sell {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .pnl-pos { color: var(--accent-green); font-weight: 700; }
        .pnl-neg { color: var(--accent-red); font-weight: 700; }

        .btn-delete {
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1.1rem;
            transition: color 0.2s ease;
        }

        .btn-delete:hover {
            color: var(--accent-red);
        }

        .empty-text {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <!-- 3D Canvas Background -->
    <div id="canvas-container"></div>

    <div class="container">
        <!-- Header -->
        <header>
            <div class="logo">
                <div class="logo-icon"></div>
                AI TRADING LAB & JOURNAL
            </div>
            <div class="badge-live">SYSTEM ACTIVE</div>
        </header>

        <!-- Top Analytics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Logged Trades</div>
                <div class="stat-value" id="stat-total">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Win Ratio</div>
                <div class="stat-value" id="stat-winrate" style="color: var(--accent-cyan);">0.0%</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Cumulative P&L</div>
                <div class="stat-value" id="stat-pnl">$0.00</div>
            </div>
        </div>

        <!-- Main Workspace -->
        <div class="main-content">
            <!-- Trade Entry Form -->
            <div class="panel">
                <div class="panel-header">Log New Execution</div>
                <form id="journal-form">
                    <div class="form-group">
                        <label>Date</label>
                        <input type="date" id="trade-date" required>
                    </div>

                    <div class="form-group">
                        <label>Asset / Instrument</label>
                        <input type="text" id="trade-pair" placeholder="e.g. XAU/USD, EUR/USD" required>
                    </div>

                    <div class="form-group">
                        <label>Direction</label>
                        <select id="trade-direction">
                            <option value="BUY">BUY / LONG</option>
                            <option value="SELL">SELL / SHORT</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Position Size (Lots)</label>
                        <input type="number" step="0.01" id="trade-size" placeholder="1.00" required>
                    </div>

                    <div class="form-group">
                        <label>Profit / Loss ($)</label>
                        <input type="number" step="0.01" id="trade-pnl" placeholder="e.g. +250 or -100" required>
                    </div>

                    <div class="form-group">
                        <label>Setup Strategy & Notes</label>
                        <textarea id="trade-notes" rows="3" placeholder="Key triggers, Market Structure, Risk management..."></textarea>
                    </div>

                    <button type="submit" class="btn-submit">Commit Record</button>
                </form>
            </div>

            <!-- History Table -->
            <div class="panel">
                <div class="panel-header">Execution Records</div>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Asset</th>
                                <th>Type</th>
                                <th>Lots</th>
                                <th>P&L ($)</th>
                                <th>Strategy / Notes</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="trade-table-body"></tbody>
                    </table>
                    <div id="empty-state" class="empty-text">No trades committed yet. Log a position to view analytics.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Three.js Engine for 3D Background -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // --- 3D Scene Setup ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x030712, 0.025);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 4, 16);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // --- Sci-Fi Grid Floor ---
        const gridHelper = new THREE.GridHelper(50, 50, 0x38bdf8, 0x1e293b);
        gridHelper.position.y = -3;
        scene.add(gridHelper);

        // --- 3D Holographic Candlesticks ---
        const candleGroup = new THREE.Group();
        const candleCount = 20;
        const spacing = 1.3;
        let lastY = 0;

        for (let i = 0; i < candleCount; i++) {
            const isGreen = Math.random() > 0.45;
            const height = Math.random() * 2.5 + 0.8;
            const color = isGreen ? 0x22c55e : 0xef4444;

            const bodyGeo = new THREE.BoxGeometry(0.5, height, 0.5);
            const bodyMat = new THREE.MeshBasicMaterial({
                color: color,
                wireframe: true
            });
            const candle = new THREE.Mesh(bodyGeo, bodyMat);

            const yPos = lastY + (isGreen ? height / 2 : -height / 2);
            lastY = yPos;
            candle.position.set((i - candleCount / 2) * spacing, yPos * 0.25, 0);

            const wickGeo = new THREE.CylinderGeometry(0.03, 0.03, height + 1.2, 6);
            const wickMat = new THREE.MeshBasicMaterial({ color: color });
            const wick = new THREE.Mesh(wickGeo, wickMat);
            wick.position.copy(candle.position);

            candleGroup.add(candle);
            candleGroup.add(wick);
        }
        scene.add(candleGroup);

        // --- Floating Ambient Particles ---
        const pGeo = new THREE.BufferGeometry();
        const pCount = 250;
        const pPos = new Float32Array(pCount * 3);

        for(let i = 0; i < pCount * 3; i++) {
            pPos[i] = (Math.random() - 0.5) * 35;
        }
        pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));

        const pMat = new THREE.PointsMaterial({
            color: 0x38bdf8,
            size: 0.07,
            transparent: true,
            opacity: 0.5
        });
        const particles = new THREE.Points(pGeo, pMat);
        scene.add(particles);

        // --- Animation Loop ---
        function animate() {
            requestAnimationFrame(animate);
            candleGroup.rotation.y += 0.002;
            particles.rotation.y -= 0.0005;
            candleGroup.position.y = Math.sin(Date.now() * 0.001) * 0.2;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- Journal Storage & Analytics Script ---
        let trades = JSON.parse(localStorage.getItem('ai_trading_journal_data')) || [];

        const form = document.getElementById('journal-form');
        const tableBody = document.getElementById('trade-table-body');
        const emptyState = document.getElementById('empty-state');

        const statTotal = document.getElementById('stat-total');
        const statWinrate = document.getElementById('stat-winrate');
        const statPnl = document.getElementById('stat-pnl');

        document.getElementById('trade-date').valueAsDate = new Date();

        function syncData() {
            localStorage.setItem('ai_trading_journal_data', JSON.stringify(trades));
            renderUI();
        }

        function renderUI() {
            tableBody.innerHTML = '';
            
            if (trades.length === 0) {
                emptyState.style.display = 'block';
            } else {
                emptyState.style.display = 'none';
            }

            let totalPnl = 0;
            let winCount = 0;

            trades.forEach((trade, index) => {
                const pnlVal = parseFloat(trade.pnl);
                totalPnl += pnlVal;
                if (pnlVal > 0) winCount++;

                const row = document.createElement('tr');
                const isPos = pnlVal >= 0;

                row.innerHTML = `
                    <td>${trade.date}</td>
                    <td><strong>${trade.pair.toUpperCase()}</strong></td>
                    <td><span class="badge ${trade.direction === 'BUY' ? 'badge-buy' : 'badge-sell'}">${trade.direction}</span></td>
                    <td>${trade.size}</td>
                    <td class="${isPos ? 'pnl-pos' : 'pnl-neg'}">${isPos ? '+' : ''}$${pnlVal.toFixed(2)}</td>
                    <td style="color: var(--text-muted);">${trade.notes || '-'}</td>
                    <td><button class="btn-delete" onclick="removeTrade(${index})">✕</button></td>
                `;
                tableBody.appendChild(row);
            });

            statTotal.textContent = trades.length;
            const winRate = trades.length > 0 ? ((winCount / trades.length) * 100).toFixed(1) : 0;
            statWinrate.textContent = `${winRate}%`;
            statPnl.textContent = `${totalPnl >= 0 ? '+' : ''}$${totalPnl.toFixed(2)}`;
            statPnl.className = `stat-value ${totalPnl >= 0 ? 'pnl-pos' : 'pnl-neg'}`;
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const entry = {
                date: document.getElementById('trade-date').value,
                pair: document.getElementById('trade-pair').value,
                direction: document.getElementById('trade-direction').value,
                size: document.getElementById('trade-size').value,
                pnl: document.getElementById('trade-pnl').value,
                notes: document.getElementById('trade-notes').value
            };

            trades.unshift(entry);
            syncData();

            document.getElementById('trade-pair').value = '';
            document.getElementById('trade-size').value = '';
            document.getElementById('trade-pnl').value = '';
            document.getElementById('trade-notes').value = '';
        });

        function removeTrade(index) {
            trades.splice(index, 1);
            syncData();
        }

        renderUI();
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
    
