from blog.models.base import db
from datetime import datetime

role_authority = db.Table('role_authority',
                          db.Column('role_name', db.String(255), db.ForeignKey('role.name'), primary_key=True),
                          db.Column('authority_name', db.String(255), db.ForeignKey('authority.name'),
                                    primary_key=True),
                          db.Column('modified', db.DateTime, db.ColumnDefault(datetime.now()), nullable=False),
                          db.Column('create', db.DateTime, db.ColumnDefault(datetime.now()))
                          )


class Role(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    modified = db.Column(db.DateTime, nullable=False)
    create = db.Column(db.DateTime, nullable=False)
    authorities=db.relationship('Authority',secondary=role_authority,backref=('roles'))
