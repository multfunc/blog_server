from blog.models.base import db
from datetime import datetime


class LogRequestHttp(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    ip_original = db.Column(db.String(128), nullable=False)
    ip_destination = db.Column(db.String(128), nullable=False)
    host = db.Column(db.String(128), nullable=False)
    uri = db.Column(db.String(1024))
    method = db.Column(db.String(10), nullable=False)
    request_data = db.Column(db.String(1024))
    user_agent = db.Column(db.String(256))
    port_destination = db.Column(db.Integer)
    referrer = db.Column(db.String(255))
    create = db.Column(db.DateTime, nullable=False,default=datetime.now)
