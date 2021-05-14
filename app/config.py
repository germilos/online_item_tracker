import os

basedir = os.path.abspath(os.path.dirname(__file__))
mongodb_local_base = 'mongodb://localhost:27017/'
database_name = 'onlineitemtracker'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    MONGODB_SETTINGS = {
        'db': 'onlineitemtracker',
        'host': 'localhost',
        'port': 27017
    }

# class TestingConfig(BaseConfig):
#     DEBUG = True
#     TESTING = True
#     BCRYPT_LOG_ROUNDS = 4
#     SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
#     PRESERVE_CONTEXT_ON_EXCEPTION = False


# class ProductionConfig(BaseConfig):
#     SECRET_KEY = 'my_precious'
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
