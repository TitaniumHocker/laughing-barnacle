# -*- coding: utf-8 -*-
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
from flask_babelex import Babel
from flask_mail import Mail
from flask_socketio import SocketIO
from flask import request, current_app
from lb.models import db, User, Role


migrate = Migrate()
security = Security()
mail = Mail()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
babel = Babel()
io = SocketIO()


@babel.localeselector
def get_locale():
    return request.args.get('lang', current_app.config['BABEL_DEFAULT_LOCALE'])
