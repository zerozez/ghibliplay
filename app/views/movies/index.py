"""
    Movie module contains movie endpoints and their helper functions
"""

from collections import defaultdict

from flask import render_template, current_app, abort
from sqlalchemy.exc import SQLAlchemyError

from app.blueprints import movies

from app.extensions import cache
from app.extensions import db

from app.models.cast import Cast
from app.models.movie import Movie
from app.models.people import Character

from app.tools.requests import get_json, InvalidResponse


@movies.route('/')
@cache.cached()
def index():
    """Movie index endpoint renders a page with all Ghibli movies and people in
    them.
    The endpoints tries to collect all information about movies from
    3d party API and store it in the database for the further use. Any future
    calls verify information about fimls with the database and update if
    new films are in the list

    Returns:
        Rendered templated page. Renponse is cached between calls for the
        default number of seconds set in Caching Configuration.

        If a error occured, returns error page.
    """
    if 'GHIBLI_API_URL' not in current_app.config:
        abort(500, "Application hasn't been fully configured. \
              GHIBLI_API_URL is missing")

    api_url = current_app.config['GHIBLI_API_URL']

    try:
        num_films = Movie.query.count()
        films = get_fimls(api_url)

        # Update our records if we're missing some
        if num_films != len(films):
            update_films(api_url, films[num_films:])

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(e)
        abort(500, "Problem with database connection")

    except InvalidResponse as e:
        current_app.logger.error(e)

    except Exception as e:
        current_app.logger.error(e)
        abort(500, "Internal Server Error")

    # Even if we have InvalidResponse from Ghibli API we can use our records
    try:
        # Select all films and their 'people' cast
        casts = db.session.query(
            Movie.name, Character.name
        ).outerjoin(
            Cast, Cast.movie_id == Movie.id
        ).outerjoin(
            Character, Character.id == Cast.character_id
        ).all()

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(e)
        abort(500, "Problem with database connection")

    data = defaultdict(list)
    for row in casts:
        data[row[0]].append(row[1])

    return render_template('index.html', movies=data)


def get_fimls(url):
    """get_fimls gathers information about films from 3d-party API and returns
    it as a json object.

    Parameters:
        url (text) -- API Base URL

    Returns:
        Json object with gathered data. Every object contains next fields:
            id, title and release_data
        If something goes wrong with the request InvalidResponse exception will
        be raised.
    """
    data = get_json(f'{url}/films?fields=id,title,release_date')

    if data.status_code != 200:
        raise InvalidResponse(data.status_code, data.text)

    return data.json()


def get_people(url):
    """get_people gathers information about people from 3d-party API and
    returns it as a json object.

    Parameters:
        url (text) -- API Base URL

    Returns:
        Json object with gathered data. Every object contains next fields:
            id, name and films as a unique identificators (uuid4 standard)
        If something goes wrong with the request InvalidResponse exception will
        be raised.
    """
    data = get_json(f'{url}/people?fields=id,name,films')
    substr = '/films/'

    if data.status_code != 200:
        raise InvalidResponse(data.status_code)

    # Converting data's film url in film id
    out = []
    for r in data.json():
        films = []

        for film in r["films"]:
            pos = film.find(substr) + len(substr)
            films.append(film[pos:])

        r["films"] = films
        out.append(r)

    return out


def get_cast(people, film):
    """get_cast creates a list of all people in specific film

    Parameters:
        people (list) -- List of people(id, name, films)
        film (str) -- Specific film id as a search parameter

    Returns:
        List of people who have records in casting in the film
    """
    data = []

    for person in people:
        if film in person['films']:
            data.append(person)

    return data


def update_films(url, base):
    """ update_films add missing films, people and their connections in the
    database.

    Parameters:
        url (str) -- API Base URL

    """
    people = get_people(url)

    # Gathering information about new films
    for film in base:
        r = Movie(film['id'], film['title'], int(film['release_date']))
        db.session.add(r)

        cast = get_cast(people, r.id)
        for member in cast:
            # Update our Character list
            if Character.query.filter_by(id=member['id']).first() is None:
                m = Character(member['id'], member['name'])
                db.session.add(m)

            c = Cast(r.id, member['id'])
            db.session.add(c)

    db.session.commit()
