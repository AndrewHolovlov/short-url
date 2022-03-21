import datetime

from flask import redirect, request, jsonify
from flask_restful import Resource

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range

from api.models.shortener import ShortUrl
from api.database import db


class CreateShortUrlParamsSchema(Schema):
    long_url = fields.Str(required=True)
    life_span = fields.Int(default=90, load_default=90,
                           validate=[Range(min=1, max=256, error="value must be between 1 and 256")])


class CreateShortUrlResponseSchema(Schema):
    long_url = fields.Str()
    short_url = fields.Str()
    expiry_at = fields.DateTime()


class ClickStatisticsSchema(Schema):
    number_of_clicks = fields.Int()


class ErrorSchema(Schema):
    message = fields.Str()


post_schema = CreateShortUrlParamsSchema()


class CreateShortUrl(MethodResource, Resource):
    @doc(description='Create short url', tags=['Short url'])
    @use_kwargs(CreateShortUrlParamsSchema, location=('json'), apply=False)
    @marshal_with(CreateShortUrlResponseSchema, description='Create short url', code=201)
    def post(self, **kwargs):
        json_data = request.get_json()
        try:
            data = post_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        obj = ShortUrl(long_url=data['long_url'], life_span=data['life_span'])
        db.session.add(obj)
        db.session.commit()

        obj.token = ShortUrl.generate_token(url=obj.long_url, _id=obj.id)
        db.session.commit()

        return obj, 201


class RedirectByShortUrl(MethodResource, Resource):
    @doc(description='Redirect by short url', tags=['Short url'])
    @marshal_with(None, description='Redirect by short url', code=302)
    @marshal_with(ErrorSchema, description='Token not found', code=404)
    @marshal_with(ErrorSchema, description='Token expired/invalid', code=498)
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


class ClickStatistics(MethodResource, Resource):
    @doc(description='Click statistics', tags=['Short url'])
    @marshal_with(ClickStatisticsSchema, description='Click statistics', code=200)
    @marshal_with(ErrorSchema, description='Token not found', code=404)
    def get(self, token):
        obj = db.session.query(ShortUrl).filter(ShortUrl.token == token).first()

        if obj:
            return {'number_of_clicks': obj.number_of_clicks}, 200
        else:
            return {'message': 'NOT FOUND'}, 404







