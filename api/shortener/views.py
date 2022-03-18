import datetime

from flask import redirect
from flask_restful import Resource, reqparse

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from api.models.shortener import ShortUrl
from api.database import db


def life_span(life_span_int):
    if isinstance(life_span_int, int):
        if life_span_int in range(1, 256):
            return life_span_int
        else:
            raise ValueError('life_span must be between 1 and 256')
    else:
        raise ValueError('life_span must be integer')


post_parser = reqparse.RequestParser()
post_parser.add_argument('long_url', type=str, help='long_url is required', required=True)
post_parser.add_argument('life_span', type=life_span, default=90)


class CreateShortUrlParamsSchema(Schema):
    long_url = fields.Str()
    life_span = fields.Int()


class CreateShortUrlResponseSchema(Schema):
    long_url = fields.Str()
    short_url = fields.Str()
    expiry_at = fields.DateTime()


class CreateShortUrl(MethodResource, Resource):
    @doc(description='Create short url', tags=['Short url'])
    @use_kwargs(CreateShortUrlParamsSchema, location=('json'))
    @marshal_with(CreateShortUrlResponseSchema,
                  description='Update expiry time if expiry time expired else return short url', code=200)
    @marshal_with(CreateShortUrlResponseSchema, description='Create short url', code=201)
    def post(self, **kwargs):
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


class RedirectByShortUrl(MethodResource, Resource):
    @doc(description='Redirect by short url', tags=['Short url'])
    @marshal_with(None, description='Redirect by short url', code=302)
    @marshal_with(None, description='Token not found', code=404)
    @marshal_with(None, description='Token expired/invalid', code=498)
    def get(self, token):
        obj = db.session.query(ShortUrl).filter(ShortUrl.token == token).first()

        if obj:
            if obj.expiry_at > datetime.datetime.now():
                obj.number_of_clicks += 1
                db.session.commit()
                return redirect(obj.long_url, code=302)
            else:
                return {'message': 'Token expired/invalid'}, 498
        else:
            return {'message': 'NOT FOUND'}, 404








