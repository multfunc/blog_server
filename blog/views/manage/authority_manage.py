from flask import json, jsonify, Blueprint, current_app, request
from flask_cors import CORS
from datetime import datetime

from blog.utils.rsa_utils import rsa_utils
from blog.models.base import db
from blog.models.user_info import UserInfo
from blog.models.role import Role
from blog.models.authority import Authority

authority_manage_bp = Blueprint("authority_init", __name__, url_prefix="/blog/authority_manage")
CORS(authority_manage_bp)


@authority_manage_bp.route('/init/admin', methods=['POST'])
def init_admin():
    response_body = {
        "status": False,
        "data": None
    }
    try:
        role = db.session.query(Role).filter(Role.name == "超级管理员").one_or_none()  # 查询数据库中的是否有“超级管理员”这个角色
        if role:
            password = rsa_utils.encrypt_by_PKCS1_OAEP(bytes("&*($%!".encode('utf8')))
            user_info = UserInfo(account="admin", name="multfunc", password=password, modified=datetime.now(),
                                 create=datetime.now(), roles=[role])
            db.session.add_all([user_info])
            db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify(response_body)


@authority_manage_bp.route('init', methods=['POST'])
def init():
    """
    初始化：角色表、权限表
    :return:
    """
    response_body = {
        "status": False,
        "data": None
    }
    try:
        authority_modify_base = Authority(name="modify_base", resource_code=1999, modified=datetime.now(),
                                          create=datetime.now())
        authority_query_base = Authority(name="query_base", resource_code=2999, modified=datetime.now(),
                                         create=datetime.now())

        role_admin = Role(name="超级管理员", modified=datetime.now(), create=datetime.now(),
                          authorities=[authority_query_base, authority_modify_base])
        role_passenger = Role(name="游客", modified=datetime.now(), create=datetime.now(),
                              authorities=[authority_query_base])

        db.session.add_all([
            role_admin, role_passenger
        ])
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify(response_body)
