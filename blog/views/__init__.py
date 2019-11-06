from flask import Flask
from blog.views.test import test_bp
from blog.views.user_token import user_token_bp


def init_app(app: Flask):
    app.register_blueprint(test_bp)
    app.register_blueprint(user_token_bp)
