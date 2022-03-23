from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from flask import Flask, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api import database
from api.shortener.views import CreateShortUrl, RedirectByShortUrl, ClickStatistics
from api.accounts.views import SignUpView, LoginView, RefreshTokenView, Test
from api.models.accounts import User

# create Flask app
app = Flask(__name__.split('.')[0])
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize db
database.init_app(app)


@app.before_first_request
def create_database():
    database.drop_db()
    database.create_db()


# Add resource
api.add_resource(CreateShortUrl, '/')
api.add_resource(RedirectByShortUrl, '/<string:token>')
api.add_resource(ClickStatistics, '/<string:token>/statistics')
api.add_resource(SignUpView, '/account/signup')
api.add_resource(LoginView, '/account/login')
api.add_resource(RefreshTokenView, '/accounts/token/refresh')
api.add_resource(Test, '/account/test')


app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Short url',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_UI_URL': '/doc/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

docs.register(CreateShortUrl)
docs.register(RedirectByShortUrl)
docs.register(ClickStatistics)


# Automatic User Loading JWTManager
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Errors handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



