from flask import Flask

def init_app(app:Flask):
    app.config.from_pyfile('settings/settings.py')