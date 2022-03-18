import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from . import db


class ShortUrl(db.Model):
    __tablename__ = 'shorturl'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(7))
    long_url = db.Column(db.String)
    create_at = db.Column(db.DateTime, server_default=db.func.now())
    clicked = db.Column(db.Integer, default=0)
    life_span = db.Column(db.Integer, default=90)

    @hybrid_property
    def expiry_at(self):
        return self.create_at + datetime.timedelta(days=self.life_span)

    @hybrid_property
    def short_url(self):
        return 'http://192.168.1.2:8080/' + self.token
