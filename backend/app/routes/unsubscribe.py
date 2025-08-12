
import os, hmac, hashlib
from flask import Blueprint, request, jsonify
from ..models import db, Suppression

unsub_bp = Blueprint("unsub", __name__)
SECRET = os.getenv("SECRET_KEY","change_this")

def valid(email, token):
    mac = hmac.new(SECRET.encode(), email.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, token or "")

@unsub_bp.route("/unsubscribe", methods=["GET","POST"])
def unsubscribe():
    email = request.values.get("email","").strip().lower()
    token = request.values.get("token","")
    if not email or not valid(email, token):
        return "Invalid unsubscribe link", 400
    if not Suppression.query.filter_by(email=email).first():
        db.session.add(Suppression(email=email, reason="user_unsubscribe"))
        db.session.commit()
    return "You have been unsubscribed. We're sorry to see you go."
