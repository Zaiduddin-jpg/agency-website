import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

SENDER_EMAIL = "zaiduddin123z@gmail.com"
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    # Preflight CORS check for browsers
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200

    try:
        # Safely parse incoming data (fallback if headers are strange)
        data = request.get_json(silent=True) or {}
        name = data.get('name', 'N/A')
        email = data.get('email', 'N/A')
        issue = data.get('issue', 'N/A')

        if not APP_PASSWORD:
            return jsonify({"error": "Deploy Error: Missing GMAIL_APP_PASSWORD in Render Settings"}), 500

        msg = MIMEMultipart()
        msg["From"] = f"NexGen Website <{SENDER_EMAIL}>"
        msg["To"] = SENDER_EMAIL
        msg["Subject"] = f"New Audit Request from {name}"
        
        body = f"New Meeting/Audit Request!\n\nName: {name}\nEmail: {email}\nBottleneck: {issue}\n\nPlease reach out to them as soon as possible.\n"
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as s:
            s.starttls()
            s.login(SENDER_EMAIL, APP_PASSWORD)
            s.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
            
        return jsonify({"success": True})

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Backend Crash Log:\n{error_trace}")
        return jsonify({"error": str(e), "trace": error_trace}), 500

if __name__ == '__main__':
    app.run(port=8080)
