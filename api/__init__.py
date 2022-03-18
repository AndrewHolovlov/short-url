from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from flask import Flask, jsonify, make_response
from flask_restful import Api

from api import database
from api.shortener.views import CreateShortUrl, RedirectByShortUrl

# create Flask app
app = Flask(__name__.split('.')[0])
api = Api(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize db
database.init_app(app)


@app.before_first_request
def create_database():
    database.drop_db()
    database.create_db()
    pass


# Add resource
api.add_resource(CreateShortUrl, '/')
api.add_resource(RedirectByShortUrl, '/<string:token>')


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


# Errors handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



