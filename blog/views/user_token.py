import json as python_json
from flask import json, jsonify, Blueprint, current_app, request
from flask_cors import *
from datetime import datetime

from blog.utils.rsa_utils import rsa_utils

from blog.models.base import db
from blog.models.user_info import UserInfo
from blog.models.role import Role
from blog.models.authority import Authority

user_token_bp = Blueprint('user_token', __name__, url_prefix='/blog/user_token')


@user_token_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    登录
    :return:
    """
    response_body = {
        "status": False,
        "data": {
            "message": "温馨提示：请重新核对账号与密码 ^_^"
        }
    }

    request_body = json.loads(request.data)
    print(request_body)
    # password=rsa_utils.decrypt(request_data.get("en_password"))
    # print("明文密码",password)

    account = request_body.get("account")  # 请求中携带的用户名
    en_password = request_body.get("en_password")  # 请求中携带的加过密的密码
    password = rsa_utils.decrypt_by_PKCS1_v1_5(en_password)  # 解密之后的 bytes 类型密码
    user_info = db.session.query(UserInfo).filter(UserInfo.account == account).one_or_none()  # 查询数据中是否有该用户

    if user_info:  # 不存在该用户
        db_password = rsa_utils.decrypt_by_PKS1_OAEP(user_info.password)  # 数据中用户密码解密后的明文
        response_body["status"] = True if password == db_password else False  # 密码是否正确
    else:
        response_body["status"] = False
    return jsonify(response_body)


@user_token_bp.route('/register', methods=['POST'])
@cross_origin()  # 置于route后
def add_user():
    """
    添加账号 需要配合前端JSEncrypt
    :return:
    """
    response_body = {
        "status": False,
        "data": None
    }
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    try:
        account = request_body.get("account")
        en_password = request_body.get("en_password")
        password = rsa_utils.decrypt_by_PKCS1_v1_5(en_password)
        password = rsa_utils.encrypt_by_PKCS1_OAEP(password)
        user_info = [UserInfo(account=account, password=password, name="test_name", last_login=datetime.now(),
                              modified=datetime.now(), create=datetime.now())]
        db.session.add_all(user_info)
        db.session.commit()
    except Exception as e:
        print(e)
    return jsonify(response_body)
