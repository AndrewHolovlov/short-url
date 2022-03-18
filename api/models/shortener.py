import datetime

from hashids import Hashids
from sqlalchemy.ext.hybrid import hybrid_property

from . import db


class ShortUrl(db.Model):
    __tablename__ = 'shorturl'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(7))
    long_url = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    expiry_at = db.Column(db.DateTime)
    number_of_clicks = db.Column(db.Integer, default=0)

    def __init__(self, long_url, life_span):
        self.token = self.generate_token(url=long_url)
        self.long_url = long_url
        self.created_at = datetime.datetime.now()
        self.expiry_at = self.created_at + datetime.timedelta(days=life_span)

    @hybrid_property
    def short_url(self):
        return 'http://192.168.1.2:8080/' + self.token

    @staticmethod
    def generate_token(url: str):
        hashids = Hashids(salt=url, min_length=7)
        return hashids.encode(1)
