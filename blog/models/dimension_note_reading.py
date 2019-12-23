from blog.models.base import db


class DimensionNoteReading(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    origin_name_book = db.Column(db.String(255), nullable=False)  # 书名
    origin_author_book = db.Column(db.String(255), nullable=False)  # 作者
    origin_page_book = db.Column(db.String(255), nullable=False)  # 页码
    note = db.Column(db.String(255), nullable=False)  # 摘录
    category = db.Column(db.String(255), nullable=False)  # 类别
    modified = db.Column(db.DateTime, nullable=False)
    create = db.Column(db.DateTime, nullable=False)
