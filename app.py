import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# ---------------------------------------------------------------------------
# Employee login store (prototype only).
# For the real version, replace this with a database + hashed passwords.
# You can also override/add users via the EMPLOYEE_CREDENTIALS env var, e.g.:
#   EMPLOYEE_CREDENTIALS="alice:pass123,bob:pass456"
# ---------------------------------------------------------------------------
DEFAULT_USERS = {
    "admin": "pariman@123",
    "employee": "pariman@123",
}


def load_users():
    users = dict(DEFAULT_USERS)
    env_creds = os.environ.get("EMPLOYEE_CREDENTIALS")
    if env_creds:
        for pair in env_creds.split(","):
            if ":" in pair:
                user, pwd = pair.split(":", 1)
                users[user.strip()] = pwd.strip()
    return users


USERS = load_users()

# Cards shown on the dashboard - internal tools employees use.
CARDS = [
    {
        "title": "ITR Status",
        "description": "Check and track Income Tax Return filing status for clients.",
        "url": "https://itrstatus.parimanglobal.com/",
        "icon": "itr",
    },
    {
        "title": "Policy Portal",
        "description": "Manage and create insurance / client policies.",
        "url": "https://policypariman.onrender.com/",
        "icon": "policy",
    },
]

# Firm info shown on the login page and dashboard - edit freely.
FIRM_INFO = {
    "name": "Pariman Global",
    "tagline": "Bank Audit, RERA & Compliance Advisory",
    "about": (
        "Pariman Global is a CA-led professional services firm offering "
        "guidance on bank branch audits, LFAR reporting, NPA classification, "
        "RBI compliance, and Maharashtra RERA advisory for businesses and "
        "individuals."
    ),
    "services": [
        {"title": "Bank Branch Audit", "desc": "LFAR, NPA verification & RBI IRAC norms compliance."},
        {"title": "ITR Filing", "desc": "Income tax return preparation and filing status tracking."},
        {"title": "MahaRERA Advisory", "desc": "RERA registration, buyer advisory & compliance support."},
        {"title": "Policy Advisory", "desc": "Insurance and client policy management (coming soon)."},
    ],
    "email": "caparikshitbhadade@gmail.com",
    "phone": "+91 9105 569 555",
    "website": "https://www.parimanglobal.com",
}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return render_template("login.html", error=error, firm=FIRM_INFO)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html", user=session.get("user"), cards=CARDS, firm=FIRM_INFO
    )


@app.route("/ping")
def ping():
    return "pong", 200


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
