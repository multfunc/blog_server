from flask import Flask
from blog.views.test import test_bp


def init_app(app: Flask):
    app.register_blueprint(test_bp)
