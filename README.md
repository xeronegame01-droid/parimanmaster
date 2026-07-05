# Pariman Global – Employee Portal (Prototype)

A simple internal login portal for Pariman Global employees. After logging in,
employees see a dashboard with two cards linking to internal tools:

- **ITR Status** → https://itrstatus.parimanglobal.com/
- **Policy Portal** → https://policypariman.onrender.com/

This is a prototype: login is handled with a hardcoded username/password list
(no database yet). Good enough to demo; swap in real auth before production use.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

Default login:
- Username: `admin` or `employee`
- Password: `pariman@123`

## Deploy on Render

1. Push this folder to a GitHub repo.
2. On Render: **New +** → **Web Service** → connect the repo.
3. Settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add environment variables (Render dashboard → Environment):
   - `SECRET_KEY` – any random long string (used to sign login sessions)
   - `EMPLOYEE_CREDENTIALS` (optional) – add/override employee logins, format:
     `alice:herpassword,bob:hispassword`
5. Deploy. Render will give you a URL like `https://pariman-portal.onrender.com`.

## Notes for the real version (later)

- Replace the hardcoded `USERS` dict with a proper database + hashed passwords
  (e.g. `werkzeug.security.generate_password_hash`).
- Consider adding "forgot password" / employee self-signup if needed.
- Add HTTPS-only cookies (`SESSION_COOKIE_SECURE = True`) once served over HTTPS
  (Render gives you HTTPS by default, so this is easy to turn on).
- Add more cards to the `CARDS` list in `app.py` as more internal tools go live.
