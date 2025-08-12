import os, hmac, hashlib
from urllib.parse import urlencode
from flask import Blueprint, request, redirect
from ..models import db, Shop
import requests

auth_bp = Blueprint("auth", __name__)
API_KEY = os.getenv("SHOPIFY_API_KEY")
API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SCOPES = os.getenv("SCOPES")
REDIRECT_URI = os.getenv("REDIRECT_URI")
APP_BASE_URL = os.getenv("APP_BASE_URL")

def verify_hmac(params):
    h = params.pop("hmac", None)
    message = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    digest = hmac.new(API_SECRET.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    return h == digest

@auth_bp.route("/shopify/install")
def install():
    shop = request.args.get("shop")
    if not shop:
        return "Missing shop", 400
    install_url = f"https://{shop}/admin/oauth/authorize?" + urlencode({
        "client_id": API_KEY,
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI
    })
    return redirect(install_url)

@auth_bp.route("/shopify/callback")
def callback():
    params = dict(request.args)
    if not verify_hmac(params.copy()):
        return "HMAC verification failed", 401

    shop = params.get("shop")
    code = params.get("code")
    token_url = f"https://{shop}/admin/oauth/access_token"
    resp = requests.post(token_url, json={"client_id": API_KEY, "client_secret": API_SECRET, "code": code})
    resp.raise_for_status()
    access_token = resp.json()["access_token"]

    s = Shop.query.filter_by(shop=shop).first()
    if s: s.access_token = access_token
    else: db.session.add(Shop(shop=shop, access_token=access_token))
    db.session.commit()

    # Register webhooks
    for topic, path in [
        ("customers/create", "/webhooks/customers_create"),
        ("checkouts/update", "/webhooks/checkouts_update"),
        ("app/uninstalled", "/webhooks/app_uninstalled"),
    ]:
        register_webhook(shop, access_token, topic, APP_BASE_URL + path)

    return "App installed. You can close this window."

def register_webhook(shop, token, topic, callback_url):
    url = f"https://{shop}/admin/api/2023-10/webhooks.json"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    payload = {"webhook": {"topic": topic, "address": callback_url, "format": "json"}}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception:
        pass