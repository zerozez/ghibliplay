"""
    Initial module with create_app factory for the GhibliPlay application
"""
from importlib import import_module

from flask import Flask

from app import blueprints
from app.extensions import db, cache, data_models


def create_app():
    """GhibliPlay flask application factory. Uses for initialize data models,
    register blueprints and apply right configuration for current execution.


    Arguments:
        running_type (str) -- Naming string to select running configuration.
                Can be 'production' or 'development' (default)

    Returns:
        Initialized application
    """

    app = Flask(__name__)
    running_type = app.config['ENV']

    if running_type == 'development':
        app.config.from_object('app.config.General')
    elif running_type == 'production':
        app.config.from_object('app.config.Production')
    else:
        raise ValueError("Invalid input running type")

    for model in data_models:
        import_module(f"app.models.{model}")

    for bp in blueprints.blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    db.init_app(app)
    db.create_all(app=app)

    cache.init_app(app)

    return app
