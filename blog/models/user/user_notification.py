from blog.models.base import db
from datetime import datetime


class UserNotification(db.Model):
    """
    提醒消息
    """
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)
    create = db.Column(db.DateTime, nullable=False, default=datetime.now)
