from . import db
from datetime import datetime

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.String(255), unique=True, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    welcome_enabled = db.Column(db.Boolean, default=True)
    cart_reminder_enabled = db.Column(db.Boolean, default=True)
    cart_reminder_delay_hours = db.Column(db.Integer, default=6)
    wishlist_reminder_enabled = db.Column(db.Boolean, default=True)
    wishlist_reminder_delay_hours = db.Column(db.Integer, default=24)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    shop = db.Column(db.String(255), nullable=True)
    meta = db.Column(db.JSON, nullable=True)

class ReminderQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(32), nullable=False)  # 'cart' | 'wishlist'
    shop = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    due_at = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WishlistEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Suppression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
