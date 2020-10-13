"""
    People module contains Character Data Model and its support functions
"""
import uuid

from app.extensions import db


class Character(db.Model):
    """ Character Model represents SQL Character Table which keeps information
    about People who played in Ghibli Studio movies.


    Attributes:
        id (str) -- Unique Character identification
        name (str) -- Name of the Character

    """
    id = db.Column(db.String(), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)

    __tablename__ = 'character'

    def __init__(self, id, name):
        self.id = id
        self.name = name
