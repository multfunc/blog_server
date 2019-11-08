from flask import Flask
from blog.views.test import test_bp
from blog.views.user_token import user_token_bp
from blog.views.manage.authority_manage import authority_manage_bp


def init_app(app: Flask):
    app.register_blueprint(test_bp)
    app.register_blueprint(user_token_bp)
    app.register_blueprint(authority_manage_bp)
