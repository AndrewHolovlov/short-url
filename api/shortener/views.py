import datetime

from flask import redirect
from flask_restful import Resource, reqparse, fields, marshal_with

from api.models.shortener import ShortUrl
from api.database import db


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
            if obj.expiry_at > datetime.datetime.now():
                return obj, 200
            else:
                obj.created_at = datetime.datetime.now()
                obj.expiry_at = obj.created_at + datetime.timedelta(days=args['life_span'])
                db.session.commit()
                return obj, 200
        else:
            obj = ShortUrl(long_url=args['long_url'], life_span=args['life_span'])
            db.session.add(obj)
            db.session.commit()
            return obj, 201

    def get(self, token):
        obj = db.session.query(ShortUrl).filter(ShortUrl.token == token).first()

        if obj:
            if obj.expiry_at > datetime.datetime.now():
                obj.number_of_clicked += 1
                db.session.commit()
                return redirect(obj.long_url, code=302)
            else:
                return {'message': 'Token expired/invalid'}, 498
        else:
            return {'message': 'NOT FOUND'}, 404








