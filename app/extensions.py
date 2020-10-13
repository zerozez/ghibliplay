"""
    Exstentions module keeps all global flask extensions and their data.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Extensions
db = SQLAlchemy()
cache = Cache()


# Sql Data Models
data_models = ('people', 'movie', 'cast')
