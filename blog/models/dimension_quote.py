from blog.models.base import db


class DimensionQuote(db.Model):
    origin = db.Column(db.String(255), nullable=False)
    quote = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
    create = db.Column(db.DateTime, nullable=False)
