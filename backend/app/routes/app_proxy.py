from flask import Blueprint, request
from datetime import datetime, timedelta
from ..models import db, Shop, WishlistEvent, ReminderQueue

app_proxy_bp = Blueprint("app_proxy", __name__)

@app_proxy_bp.route("/app_proxy/wishlist", methods=["POST"])
def wishlist_proxy():
    data = request.get_json(force=True)
    shop = data.get("shop")
    email = data.get("email")
    s = Shop.query.filter_by(shop=shop).first()
    if not s or not s.wishlist_reminder_enabled: return "OK", 200
    we = WishlistEvent(shop=shop, customer_email=email, product_id=data.get("product_id"),
                       title=data.get("title"), image=data.get("image"))
    db.session.add(we); db.session.commit()

    from datetime import timedelta, datetime
    due = datetime.utcnow() + timedelta(hours=s.wishlist_reminder_delay_hours or 24)
    db.session.add(ReminderQueue(
        kind="wishlist", shop=shop, customer_email=email,
        payload={"product_id": data.get("product_id"), "title": data.get("title"), "image": data.get("image")},
        due_at=due
    ))
    db.session.commit()
    return "OK", 200