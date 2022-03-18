from flask import Flask, jsonify, make_response

from api import database
from api.shortener.views import shortener_module


# create Flask app
app = Flask(__name__.split('.')[0])
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
database.init_app(app)


@app.before_first_request
def create_database():
    database.drop_db()
    database.create_db()


# Register blueprints
app.register_blueprint(shortener_module)


# Errors handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



