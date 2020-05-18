# -*- coding: utf-8 -*-
from flask import Flask
from config import configurations as cfgs
from lb.exceptions import InvalidConfigurationType
from lb.extensions import migrate, security, user_datastore, babel, mail, io
from lb.forms import CustomSendConfirmationForm
from lb.blueprints import public
from lb.models import db
from lb.admin import admin
from lb import events


def make_io_app(mode='dev'):
    try:
        cfg = cfgs[mode]
    except KeyError:
        raise InvalidConfigurationType(
            'Unknown config type, try "prod", "dev" or "test".'
        )
    app = Flask(__name__)
    app.config.from_object(cfg)
    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, user_datastore,
                      send_confirmation_form=CustomSendConfirmationForm)
    mail.init_app(app)
    babel.init_app(app)
    admin.init_app(app)
    io.init_app(app)

    app.register_blueprint(public, url_prefix='/')
    # return app
    return app, io


def create_app(*args, **kwargs):
    app, _ = make_io_app(*args, **kwargs)
    return app
