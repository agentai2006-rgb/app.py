import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Render-এর Environment Variables থেকে জিমেইল ইনফো নেওয়া হবে
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")     # আপনার জিমেইল
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD") # জিমেইলের ১৬ ডিজিটের App Password

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Business Manager - Simple SMTP Agent</title>
    <style>
        body { background: #0b0f19; color: #e2e8f0; font-family: Arial, sans-serif; padding: 20px; }
        .container { max-width: 700px; margin: auto; }
        .agent-card { background: #161f30; border-radius: 12px; padding: 20px; border: 1px solid #00f2fe; margin-bottom: 20px; }
        .status { color: #00ff88; font-weight: bold; }
        .log-box { background: #090d16; border-radius: 8px; padding: 15px; height: 160px; overflow-y: auto; font-family: monospace; color: #00f2fe; margin-bottom: 20px; border: 1px solid #1f293d; }
        .input-group { display: flex; flex-direction: column; gap: 10px; background: #161f30; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); }
        input, textarea { background: #0f1522; border: 1px solid #232f48; padding: 12px; color: #fff; border-radius: 8px; outline: none; }
        button { background: linear-gradient(45deg, #00f2fe, #7f00ff); color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖 AI Business Manager (No-API Mode)</h2>
        
        <div class="agent-card">
            <h3>Agent Status: <span class="status">LIVE ON RENDER</span></h3>
            <p>এজেন্ট সম্পূর্ণ প্রস্তুত। জিমেইল এপিআই ছাড়াই সরাসরি এসটিএমপি (SMTP) প্রটোকল ব্যবহার করে কাজ করছে।</p>
        </div>

        <h4>📋 Live Agent Logs:</h4>
        <div class="log-box" id="agentLogs">
            [System] AI Agent Online...<br>
            [System] Connected to SMTP Mail Server...
        </div>

        <div class="input-group">
            <h4>📧 Send Email via Agent</h4>
            <input type="email" id="emailTo" placeholder="প্রাপকের ইমেইল (e.g. client@gmail.com)">
            <input type="text" id="emailSubject" placeholder="বিষয় (Subject)">
            <textarea id="emailBody" rows="3" placeholder="আপনার মেসেজ লিখুন..."></textarea>
            <button onclick="sendMail()">এজেন্টকে ইমেইল পাঠাতে বলুন</button>
        </div>
    </div>

    <script>
        function logMessage(msg) {
            const box = document.getElementById('agentLogs');
            box.innerHTML += `<br>[Agent Action] ${msg}`;
            box.scrollTop = box.scrollHeight;
        }

        async function sendMail() {
            const to = document.getElementById('emailTo').value;
            const subject = document.getElementById('emailSubject').value;
            const body = document.getElementById('emailBody').value;

            if(!to || !body) { alert("দয়া করে ইমেইল এবং মেসেজ পূরণ করুন!"); return; }

            logMessage(`ইমেইল পাঠানোর চেষ্টা চলছে -> ${to}`);

            const response = await fetch('/send-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ to, subject, body })
            });

            const result = await response.json();
            if(result.status === 'success') {
                logMessage(`✅ সফলতা! ${to} ঠিকানায় ইমেইল পাঠানো হয়েছে।`);
            } else {
                logMessage(`❌ ত্রুটি: ${result.message}`);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    to_email = data.get('to')
    subject = data.get('subject', 'Message from AI Business Agent')
    body = data.get('body')

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return jsonify({'status': 'error', 'message': 'Environment variables (SENDER_EMAIL / SENDER_PASSWORD) সেট করা নেই!'})

    try:
        # SMTP দিয়ে ইমেইল পাঠানোর কনফিগারেশন
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Gmail SMTP Server কানেকশন (Port 587)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
      
