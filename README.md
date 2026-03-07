# NexGen Automations

Elite operational infrastructure for high-growth B2B enterprise firms.

## Tech Stack
* **Frontend Design:** Vanilla HTML/CSS/JS (Cinematic DOM-Manipulation)
* **Backend Email Routing:** Python (Flask)
* **SEO Protocols:** Full technical hydration (OG, JSON-LD, Sitemap)

## Deployment Checklist
_This codebase is fully prepared for global CDN deployment._

1. **Frontend Hosting (Vercel):**
    - Connect GitHub Repository to a Vercel Account.
    - Set the Root Directory to `/`.
    - Set Build Command to blank (Static HTML).
    
2. **Backend Hosting (Render):**
    - Connect GitHub Repository to a Render Web Service.
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `gunicorn app:app`
    - Add Environment Variables:
        - `GMAIL_APP_PASSWORD` = [Your Secure App Password]

3. **Domain Binding:**
    - Buy domain name.
    - Route DNS nameservers to Vercel production deployment.
    - Change Form POST endpoint in `script.js` to match the active Render backend URL instead of localhost.

## Local Server Development
To test the entire frontend architecture locally, boot up the Python server:

```bash
pip install Flask flask-cors python-dotenv
python3 app.py
```
Open [http://localhost:8080](http://localhost:8080).
