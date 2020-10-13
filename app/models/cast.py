"""
    Cast module contains Cast Data Model and its support functions
"""
from app.extensions import db

from app.models.movie import Movie
from app.models.people import Character


class Cast(db.Model):
    """ Cast Model represents SQL Cast Table as a conjunction table between
    Movies and People in them.


    Attributes:
        movie_id (str) -- Foreign key of Movie table
        character_id (str) -- Foreign Key of Character Table

    """
    movie_id = db.Column(db.String, db.ForeignKey('movie.id'),
                         primary_key=True)
    character_id = db.Column(db.String, db.ForeignKey('character.id'),
                             primary_key=True)

    movie = db.relationship(Movie,
                            backref=db.backref("cast",
                                               cascade="all, delete-orphan")
                            )
    character = db.relationship(Character,
                                backref=db.backref(
                                    "cast",
                                    cascade="all, delete-orphan")
                                )

    __tablename__ = 'cast'

    def __init__(self, movie, person):
        self.movie_id = movie
        self.character_id = person
