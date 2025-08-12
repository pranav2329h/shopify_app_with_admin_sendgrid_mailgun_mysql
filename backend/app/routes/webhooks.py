import os, hmac, hashlib, json, base64
from datetime import datetime, timedelta
from flask import Blueprint, request
from ..models import db, Shop, EmailLog, ReminderQueue
from ..utils.emailer import send_email

webhook_bp = Blueprint("webhooks", __name__)
API_SECRET = os.getenv("SHOPIFY_API_SECRET")
APP_BASE_URL = os.getenv("APP_BASE_URL", "").rstrip("/")

def verify_webhook(req):
    hmac_header = req.headers.get("X-Shopify-Hmac-Sha256") or ""
    digest = hmac.new(API_SECRET.encode("utf-8"), req.data, hashlib.sha256).digest()
    calc = base64.b64encode(digest).decode()
    return hmac.compare_digest(hmac_header, calc)

def render_template(path, **ctx):
    html = open(path, "r", encoding="utf-8").read()
    for k, v in ctx.items():
        html = html.replace("{{" + k + "}}", str(v))
    return html

@webhook_bp.route("/webhooks/customers_create", methods=["POST"])
def customers_create():
    if not verify_webhook(request): return "Unauthorized", 401
    data = request.get_json(force=True)
    shop = request.headers.get("X-Shopify-Shop-Domain")
    s = Shop.query.filter_by(shop=shop).first()
    if not s or not s.welcome_enabled: return "OK", 200
    email = data.get("email")
    if not email: return "OK", 200
    shop_name = (shop or "").split(".")[0].replace("-", " ").title()
    logo_url = f"{APP_BASE_URL}/static/logo.svg" if APP_BASE_URL else "{{logo_url}}"
    store_url = f"https://{shop}"

    html = render_template(os.path.join(os.path.dirname(__file__), "..", "email_templates", "welcome.html"),
                           shop_name=shop_name, logo_url=logo_url, store_url=store_url)
    send_email(email, f"Welcome to {shop_name}", html)
    db.session.add(EmailLog(recipient=email, subject=f"Welcome to {shop_name}", body=html, shop=shop, meta={"type":"welcome"}))
    db.session.commit()
    return "OK", 200

@webhook_bp.route("/webhooks/checkouts_update", methods=["POST"])
def checkouts_update():
    if not verify_webhook(request): return "Unauthorized", 401
    payload = request.get_json(force=True)
    shop = request.headers.get("X-Shopify-Shop-Domain")
    s = Shop.query.filter_by(shop=shop).first()
    if not s or not s.cart_reminder_enabled: return "OK", 200

    if payload.get("completed_at") is None and payload.get("email"):
        due = datetime.utcnow() + timedelta(hours=s.cart_reminder_delay_hours or 6)
        db.session.add(ReminderQueue(
            kind="cart", shop=shop, customer_email=payload["email"],
            payload={
                "line_items": payload.get("line_items", []),
                "checkout_url": payload.get("abandoned_checkout_url") or "",
            },
            due_at=due))
        db.session.commit()
    return "OK", 200