import datetime

from flask import request
from flask_restful import Resource

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user
from marshmallow import ValidationError
from marshmallow.validate import Length, Email

from api.models.accounts import User
from api.database import db


ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = ma.auto_field(validate=[Email()])
    fist_name = ma.auto_field(validate=[Length(max=20)])
    last_name = ma.auto_field(validate=[Length(max=20)])
    password = ma.auto_field(validate=[Length(min=8, max=64)])


class LoginSchema(ma.Schema):
    email = fields.Str(validate=[Email()])
    password = fields.Str()


user_schema = UserSchema()
login_schema = LoginSchema()


class SignUpView(MethodResource, Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        if db.session.query(User).filter(User.email == data['email']).first() is not None:
            return {'message': 'Email user already exist'}, 400
        user = User(**data)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


class LoginView(MethodResource, Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = login_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user = db.session.query(User).filter(User.email == data['email']).first()
        if not user:
            return {'message': 'Email not found'}, 404
        authorized = user.check_password(password=data['password'])
        if not authorized:
            return {'message': 'Password invalid'}, 401

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


class RefreshTokenView(MethodResource, Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200


class Test(MethodResource, Resource):
    @jwt_required()
    def get(self):
        print(current_user)
        return 'Get Test'



