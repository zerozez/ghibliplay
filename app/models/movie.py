"""
    Movie module contains Movie Data Model and its support functions
"""
import uuid
import datetime

from app.extensions import db


class Movie(db.Model):
    """ Movie Model represents SQL Movie Table which keeps information about
    Ghibli movies.


    Attributes:
        id (str) -- Unique movie identification
        name (str) -- Name of the Movie
        date (datetime.date) -- Date of the Movie release. Due to missing
            information the Model keeps track only about a year of release.
            Month and day always set to 1st January

    """
    id = db.Column(db.String(), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)
    date = db.Column(db.Date(), nullable=False)

    __tablename__ = 'movie'

    def __init__(self, id, name, year):
        """ Constructor

        Parameters:
            id (str) -- Movie id
            name (str) -- Movie name
            year (int) -- Year of release
        """

        self.id = id
        self.name = name
        self.date = datetime.date(year, 1, 1)
