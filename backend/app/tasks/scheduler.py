from flask import Blueprint
from datetime import datetime
from ..models import db, ReminderQueue
from ..utils.emailer import send_email
import os

tasks_bp = Blueprint("tasks", __name__)
APP_BASE_URL = os.getenv("APP_BASE_URL", "").rstrip("/")

def render_template(path, **ctx):
    html = open(path, "r", encoding="utf-8").read()
    for k, v in ctx.items():
        html = html.replace("{{" + k + "}}", str(v))
    return html

@tasks_bp.route("/tasks/run")
def run():
    now = datetime.utcnow()
    due = ReminderQueue.query.filter_by(sent=False).filter(ReminderQueue.due_at <= now).limit(50).all()
    processed = 0
    for r in due:
        if r.kind == "cart":
            items = "".join([f"<li>{(li.get('title') or 'Item')}</li>" for li in r.payload.get("line_items", [])])
            html = render_template(os.path.join(os.path.dirname(__file__), "..", "email_templates", "cart.html"),
                                   items=items, checkout_url=r.payload.get("checkout_url",""))
            send_email(r.customer_email, "You left items in your cart", html)
        elif r.kind == "wishlist":
            p = r.payload
            image_block = f"<img src='{p.get('image','')}' alt='' style='max-width:100%;border-radius:8px'/>" if p.get('image') else ""
            html = render_template(os.path.join(os.path.dirname(__file__), "..", "email_templates", "wishlist.html"),
                                   title=p.get("title","Product"), image_block=image_block, product_url=p.get("product_url",""))
            send_email(r.customer_email, "Your wishlist item is waiting", html)
        r.sent = True
        db.session.commit()
        processed += 1
    return {"processed": processed}