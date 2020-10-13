"""
    Configurations for different run cases
"""


class General(object):
    """ Common configuration variables """

    DEBUG = True
    TESTING = False

    # SqlAlchemy configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # Using in-memory for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Caching
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # 3d Party configuration
    GHIBLI_API_URL = 'https://ghibliapi.herokuapp.com'  # API URL


class Production(General):
    """ Production specific variables"""

    DEBUG = False
