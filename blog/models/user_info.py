from blog.models.base import db
from datetime import datetime

user_info_role = db.Table('user_info_role',
                          db.Column('user_info_account', db.String(255), db.ForeignKey('user_info.account'),
                                    primary_key=True),
                          db.Column('role_name', db.String(255), db.ForeignKey('role.name'), primary_key=True),
                          db.Column('modified', db.DateTime, db.ColumnDefault(datetime.now()), nullable=False),
                          db.Column('create', db.DateTime, db.ColumnDefault(datetime.now()), nullable=False)
                          )


class UserInfo(db.Model):
    """
    用户信息表
    """
    account = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.VARBINARY(255), nullable=False)  # 貌似加密后最长128
    last_login = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
    create = db.Column(db.DateTime, nullable=False)
    roles = db.relationship('Role', secondary=user_info_role, backref=('user_infos'))
