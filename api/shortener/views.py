from datetime import datetime

from flask_restful import Resource, reqparse, abort, fields, marshal_with

from api.models.shortener import ShortUrl
from api.database import db
from .utils import get_token


post_parser = reqparse.RequestParser()
post_parser.add_argument('long_url', type=str, help='long_url is required', required=True)
post_parser.add_argument('life_span', type=int, help='life_span is required', default=90)


resource_fields = {
    'long_url': fields.String,
    'short_url': fields.String,
    'expiry_at': fields.DateTime
}


class ShortUrlView(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = post_parser.parse_args()

        obj = db.session.query(ShortUrl).filter(ShortUrl.long_url == args['long_url']).first()
        if obj:
            if obj.expiry_at < datetime.now():
                return obj, 200
            else:
                obj.token = get_token(url=args['long_url'])
                obj.create_at = datetime.now()
                obj.life_span = args['life_span']
                db.session.commit()
                return obj, 200
        else:
            obj = ShortUrl(token=get_token(url=args['long_url']), long_url=args['long_url'],
                           life_span=args['life_span'])
            db.session.add(obj)
            db.session.commit()
            return obj, 201







