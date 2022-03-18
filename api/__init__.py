from flask import Flask, jsonify, make_response
from flask_restful import Api

from api import database
from api.shortener.views import ShortUrlView

# create Flask app
app = Flask(__name__.split('.')[0])
api = Api(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.url_map
# Initialize db
database.init_app(app)


@app.before_first_request
def create_database():
    # database.drop_db()
    # database.create_db()
    pass


# Add resource
api.add_resource(ShortUrlView, '/')

# Register blueprints
# app.register_blueprint(shortener_module)


# Errors handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



