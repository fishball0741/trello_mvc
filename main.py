from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cards_controller import cards_bp
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_commands


import os


def create_app():
    app = Flask(__name__)

    # put here, not below, it's because for do it in global, for applies to all instances
    # cover the whole app for this.
    @app.errorhandler(404)
    def not_found(err):
        # str(err) = URL error,  err.get_description = html error 
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401

    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)  #using init app to put the app in, split the creation and declaration
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    app.register_blueprint(cards_bp)  #direct the link to bp link
    app.register_blueprint(auth_bp)  #direct the link to bp link
    app.register_blueprint(db_commands)  #direct the link to bp link



    return app

