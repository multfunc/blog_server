from flask import Blueprint, request, current_app
from flask_mail import Message
from datetime import datetime

# models

from blog.models.base import db
from blog.models.log.log_request_http import LogRequestHttp
from blog.models.user_info import UserInfo
from blog.models.user_status import UserStatus
from blog.models.role import Role
from blog.models.authority import Authority
from blog.models.role import Role
from blog.utils.rsa_utils import rsa_utils

request_check_bp = Blueprint('request_check', __name__, url_prefix='/')


@request_check_bp.before_app_request
def log_save():
    ip_original = request.remote_addr
    user_agent = str(request.user_agent)
    referrer = request.referrer
    ip_destination = current_app.config['IP_LOCAL']
    host = request.host
    uri = request.path
    method = request.method
    request_data = request.data
    port_destination = current_app.config['PORT_LOCAL']
    create = datetime.now()
    log_request_http = LogRequestHttp(ip_original=ip_original, ip_destination=ip_destination, host=host, uri=uri,
                                      method=method, request_data=request_data, user_agent=user_agent,
                                      port_destination=port_destination, referrer=referrer, create=create)
    try:
        db.session.add_all([log_request_http])
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


@request_check_bp.before_app_first_request
def authority_verify():
    ip_original = request.remote_addr
    # message = Message(subject='hello flask-mail', recipients=['379505061@qq.com'],
    #                   body=f'{ip_original}:flask-mail 测试代码')
    # with open(f'{current_app.config["IMAGE_DIR"]}\\static\\img\\2.jpg', mode='rb') as file:
    #     message.attach(filename='测试图片.jpg', content_type="image/jpg", data=file.read())
    # try:
    #     # current_app.mail.send(message)
    #     print("邮件发送成功")
    #     print("并没有发邮件")
    # except Exception as e:
    #     print(e)

    user_info = db.session.query(UserInfo).filter(UserInfo.account == ip_original).one_or_none()
    if user_info:
        pass
    else:
        role = db.session.query(Role).filter(Role.name == 'Guest').one_or_none()
        password = rsa_utils.encrypt_by_PKCS1_OAEP("123456".encode('utf8'))
        tmp_user_info = UserInfo(account=ip_original, name='临时游客', password=password, modified=datetime.now(),
                                 create=datetime.now(), roles=[role])
        db.session.add_all([tmp_user_info])

        #发邮件通知有新人访问
        message = Message(subject='hello flask-mail', recipients=['379505061@qq.com'],
                          body=f'{ip_original}:Hi，我来访问了')
        try:
            current_app.mail.send(message)
            print("邮件发送成功")
            print("并没有发邮件")
        except Exception as e:
            print(e)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
