from flask import Flask
from blog.models.base import db


def init_app(app: Flask):
    app.app_context().push()  # 获取app上下文 很关键
    db.init_app(app)
    # db.drop_all()
    db.create_all()
