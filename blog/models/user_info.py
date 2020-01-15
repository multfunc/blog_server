from blog.models.base import db
from blog.models.role import Role
from datetime import datetime

user_info_role = db.Table('user_info_role',
                          db.Column('user_info_account', db.String(255), db.ForeignKey('user_info.account'),
                                    primary_key=True),
                          db.Column('role_name', db.String(255), db.ForeignKey('role.name'), primary_key=True),
                          db.Column('modified', db.DateTime, db.ColumnDefault(datetime.now), nullable=False),
                          db.Column('create', db.DateTime, db.ColumnDefault(datetime.now), nullable=False)
                          )

user_info_user_status = db.Table('user_info_user_status',
                                 db.Column('user_info_account', db.String(255), db.ForeignKey('user_info.account'),
                                           primary_key=True),
                                 db.Column('user_status_auto_id', db.Integer, db.ForeignKey('user_status.auto_id'),
                                           primary_key=True),
                                 db.Column('modified', db.DateTime, db.ColumnDefault(datetime.now), nullable=False),
                                 db.Column('create', db.DateTime, db.ColumnDefault(datetime.now), nullable=False)
                                 )

user_info_user_notification = db.Table('user_info_user_notification',
                                       db.Column('user_info_account', db.String(255),
                                                 db.ForeignKey('user_info.account')),
                                       db.Column('user_notification_id', db.Integer,
                                                 db.ForeignKey('user_notification.id')),
                                       db.Column('modified', db.DateTime, default=datetime.now, nullable=False),
                                       db.Column('create', db.DateTime, default=datetime.now, nullable=False))


class UserInfo(db.Model):
    """
    用户信息表
    """
    account = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.VARBINARY(255), nullable=False)  # 貌似加密后最长128
    # last_login = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)
    create = db.Column(db.DateTime, nullable=False, default=datetime.now)
    roles = db.relationship('Role', cascade='save-update,merge,delete', secondary=user_info_role,
                            backref=('user_infos'))
    user_status = db.relationship('UserStatus', cascade='save-update,merge,delete', secondary=user_info_user_status,
                                  backref=('user_infos'))
    user_info_user_notification = db.relationship('UserNotification', cascade='all',
                                                  secondary=user_info_user_notification, backref=('user_infos'))


    def lock(self):
        # self.locked=True
        self.roles[0] = Role.query.filter_by(name='Locked').first()
        db.session.commit()

    def unlock(self):
        # self.locked=False
        self.roles[0] = Role.query.filter_by(name='User').first()
        db.session.commit()
