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

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name', 'N/A')
    email = data.get('email', 'N/A')
    issue = data.get('issue', 'N/A')

    if not APP_PASSWORD:
        return jsonify({"error": "No email password configured. Please add GMAIL_APP_PASSWORD to .env"}), 500

    msg = MIMEMultipart()
    msg["From"] = f"NexGen Website <{SENDER_EMAIL}>"
    msg["To"] = SENDER_EMAIL
    msg["Subject"] = f"New Audit Request from {name}"
    
    body = f"""New Meeting/Audit Request!

Name: {name}
Email: {email}
Bottleneck: {issue}

Please reach out to them as soon as possible.
"""
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(SENDER_EMAIL, APP_PASSWORD)
            s.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
