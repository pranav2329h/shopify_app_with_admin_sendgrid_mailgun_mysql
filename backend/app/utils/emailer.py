
import os, smtplib, requests, hmac, hashlib
from email.mime.text import MIMEText
from ..models import db, Suppression

PROVIDER = os.getenv("EMAIL_PROVIDER", "smtp").lower()  # smtp | sendgrid | mailgun
APP_BASE_URL = os.getenv("APP_BASE_URL", "").rstrip("/")

def _unsub_headers(email):
    secret = os.getenv("SECRET_KEY","change_this")
    token = hmac.new(secret.encode(), email.encode(), hashlib.sha256).hexdigest()
    link = f"{APP_BASE_URL}/unsubscribe?email={email}&token={token}" if APP_BASE_URL else ""
    headers = {}
    if link:
        headers["List-Unsubscribe"] = f"<{link}>"
        headers["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    return headers, link

def send_email(recipient: str, subject: str, html_body: str):
    # Suppression check
    if Suppression.query.filter_by(email=recipient.lower()).first():
        return

    if PROVIDER == "sendgrid":
        return _sendgrid(recipient, subject, html_body)
    elif PROVIDER == "mailgun":
        return _mailgun(recipient, subject, html_body)
    else:
        return _smtp(recipient, subject, html_body)

def _smtp(recipient, subject, html):
    host = os.getenv("SMTP_HOST"); port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER");  pwd  = os.getenv("SMTP_PASS")
    sender = os.getenv("MAIL_FROM", user)

    msg = MIMEText(html.replace("{{unsubscribe}}", _unsub_headers(recipient)[1] or ""), "html")
    msg["Subject"] = subject; msg["From"] = sender; msg["To"] = recipient
    h, _ = _unsub_headers(recipient)
    for k, v in h.items(): msg[k] = v

    with smtplib.SMTP(host, port) as s:
        s.starttls(); s.login(user, pwd); s.sendmail(sender, [recipient], msg.as_string())

def _sendgrid(recipient, subject, html):
    key = os.getenv("SENDGRID_API_KEY")
    sender = os.getenv("MAIL_FROM")
    h, link = _unsub_headers(recipient)
    data = {
        "personalizations":[{"to":[{"email":recipient}]}],
        "from":{"email": sender},
        "subject": subject,
        "content":[{"type":"text/html","value": html.replace("{{unsubscribe}}", link or "")}],
        "headers": h
    }
    r = requests.post("https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"},
        json=data, timeout=10)
    r.raise_for_status()

def _mailgun(recipient, subject, html):
    domain = os.getenv("MAILGUN_DOMAIN")
    api = os.getenv("MAILGUN_API_KEY")
    sender = os.getenv("MAIL_FROM")
    h, link = _unsub_headers(recipient)
    data = {"from": sender, "to": [recipient], "subject": subject, "html": html.replace("{{unsubscribe}}", link or "")}
    # Include List-Unsubscribe header via Mailgun 'h:' prefix
    for k, v in h.items():
        data[f"h:{k}"] = v
    r = requests.post(f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api), data=data, timeout=10)
    r.raise_for_status()
