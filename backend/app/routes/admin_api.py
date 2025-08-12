from flask import Blueprint, request, jsonify
from ..models import db, Shop, EmailLog

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/settings/<shop>", methods=["GET","POST"])
def settings(shop):
    s = Shop.query.filter_by(shop=shop).first()
    if request.method == "GET":
        if not s: return jsonify({}), 404
        return jsonify({
            "welcome_enabled": s.welcome_enabled,
            "cart_reminder_enabled": s.cart_reminder_enabled,
            "cart_reminder_delay_hours": s.cart_reminder_delay_hours,
            "wishlist_reminder_enabled": s.wishlist_reminder_enabled,
            "wishlist_reminder_delay_hours": s.wishlist_reminder_delay_hours,
        })
    data = request.get_json(force=True)
    if not s: return jsonify({}), 404
    for f in ("welcome_enabled","cart_reminder_enabled","cart_reminder_delay_hours",
              "wishlist_reminder_enabled","wishlist_reminder_delay_hours"):
        if f in data: setattr(s, f, data[f])
    db.session.commit()
    return jsonify({"ok": True})

@admin_bp.route("/admin/logs/<shop>")
def logs(shop):
    rows = EmailLog.query.filter_by(shop=shop).order_by(EmailLog.sent_at.desc()).limit(100).all()
    return jsonify([{
        "recipient": r.recipient, "subject": r.subject, "sent_at": r.sent_at.isoformat(), "meta": r.meta
    } for r in rows])