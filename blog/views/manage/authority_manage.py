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


@authority_manage_bp.route('/init_role_and_authority', methods=['POST'])
def init_role_and_authority():
    try:
        authority_access = Authority(name="login", resource_code=1998)  # 访问权限
        authority_glance = Authority(name="glance", resource_code=1997)  # 查看权限
        authority_interact = Authority(name="interact", resource_code=1996)  # 关注用户权限
        authority_moderate = Authority(name="moderate", resource_code=1995)  # 管理资源权限，可以管理网站的用户、图片、评论、标签等资源
        authority_administer = Authority(name='administer', resource_code=1994)  # 管理用户角色、编辑网站信息等

        Authority(name="glance_normal", resource_code=1998)  # 只可以浏览页面##未登录用户
        Authority(name="glance_blocked", resource_code=1997)  # 只可以浏览页面##因违规行为被封禁账号，禁止登录的用户
        Authority(name="glance_locked", resource_code=1996)  # Follow、collect##因违规行为被锁定的用户
        Authority(name="user", resource_code=1995)  # Follow、collect、comment、upload##注册后获得的默认角色
        Authority(name="moderator",
                  resource_code=1994)  # 除了拥有普通用户的权限外，还拥有moderate权限##除了普通用户的权限外，还拥有管理网站内容的权限、负责网站内容的管理和维护
        Authority(name="administer", resource_code=0)  # 除了拥有普通用户和协管员的所有权限外，还拥有administer权限##拥有所有权限的网站管理员

        role_administrator = Role(name="Administrator",
                                  authorities=[authority_access, authority_glance, authority_interact,
                                               authority_moderate,
                                               authority_administer])
        role_moderator = Role(name="Moderator",
                              authorities=[authority_access, authority_glance, authority_interact,
                                           authority_moderate, ])
        role_user = Role(name="User", authorities=[authority_access, authority_glance, authority_interact, ])
        role_guest = Role(name='Guest', authorities=[authority_access, authority_glance, ])  # 只可以浏览页面##未登录用户
        role_locked = Role(name="Locked",
                           authorities=[authority_access, authority_glance, ])  # Follow、collect##因违规行为被锁定的用户
        role_blocked = Role(name="Blocked", authorities=[])  # 只可以浏览页面##因违规行为被封禁账号，禁止登录的用户

        db.session.add_all([
            role_administrator, role_moderator, role_user, role_guest, role_locked, role_blocked
        ])
        db.session.commit()
        return jsonify({"status":True})
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify({"status":True})


@authority_manage_bp.route('/init/admin', methods=['POST'])
def init_admin():
    """
    第2步，初始化超级管理员
    :return:
    """
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


@authority_manage_bp.route('init_role', methods=['POST'])
def init():
    """
    第一步，初始化：角色表、权限表
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
