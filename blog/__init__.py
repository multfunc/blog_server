from flask import Flask, json
from decimal import Decimal
from flask_socketio import SocketIO  # WebSocket
from flask_mail import Mail, Message
from blog import views, settings, models
from authlib.integrations.flask_oauth2 import AuthorizationServer
# from blog.oauth.server import query_client,save_token


import os

socketio = SocketIO()
mail = Mail()
server = AuthorizationServer()


def create_app():
    app = Flask(__name__)
    settings.init_app(app)  # 初始化在models初始化之前，因为有ORM设置在里面
    views.init_app(app)
    models.init_app(app)
    app.json_encoder = JSONEncoder

    # websocket support
    # app.config['SECRET_KEY']='secret string'
    # flask-socketio 内部使用了flask的session对象，所以我们要确保为程序设置了密钥（通过配置变量SECRET_KEY或app.secret_key属性）
    socketio.init_app(app)  # WebSocket
    app.config.update(  # e-mail
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=('何俊峰', os.getenv('MAIL_USERNAME'))
    )
    mail.init_app(app)  # e-mail
    app.mail = mail
    return app


class JSONEncoder(json.JSONEncoder):
    """
    json支持 decimal 类型
    """

    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)


"""
构造文件，包含程序实例
"""

# app = Flask(__name__.split('.')[0])
# views.init_app(app)
# models.init_app(app)
# settings.init_app(app)
# app.json_encoder = JSONEncoder
