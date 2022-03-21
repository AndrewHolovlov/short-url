import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'))

DEBUG = os.environ.get('DEBUG')

SECRET_KEY = os.environ.get('SECRET_KEY')

# Database
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'local.db')
SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@' \
                          f'{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')

BUNDLE_ERRORS = True


