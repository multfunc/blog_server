from blog.models.base import db
from datetime import datetime


class UserStatus(db.Model):
    """
    用户状态表
    """
    auto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), nullable=False)
    current_page = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, nullable=False,default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,default=datetime.now)
    create = db.Column(db.DateTime, nullable=False,default=datetime.now)
