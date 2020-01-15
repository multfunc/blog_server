from blog.models.base import db
from datetime import datetime


class Authority(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    resource_code = db.Column(db.Integer, nullable=False)
    modified = db.Column(db.DateTime, nullable=False,default=datetime.now)
    create = db.Column(db.DateTime, nullable=False, default=datetime.now)
