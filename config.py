# -*- coding: utf-8 -*-
from os import environ, path
import tempfile
from dotenv import load_dotenv
load_dotenv()


class BasicConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')
    API_KEY = environ.get('API_KEY')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = environ.get('SECURITY_PASSWORD_HASH')


class DevelopmentConfig(BasicConfig):
    SECURITY_EMAIL_SENDER = 'no-reply@localhost'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{path.join(path.dirname(__file__), "db.sqlite3")}'
    DEBUG=True


class ProductionConfig(BasicConfig):
    SECURITY_EMAIL_SENDER = 'noreply@lb.logovo.cloud'
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URI')


class TestingConfig(DevelopmentConfig):
    SECURITY_EMAIL_SENDER = 'noreply-test@localhost'
    TESTING = True


configurations = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
