"""
    Module for registration application views as a blueprints for their future
    use.
"""
from flask import Blueprint


# Movie blueprints
movies = Blueprint('movies', 'app.views.movies',
                   template_folder='templates', url_prefix='/movies')


# All blueprints
blueprints = (movies,)
