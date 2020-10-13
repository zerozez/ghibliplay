import pytest

from app.app import create_app


@pytest.fixture
def app(httpserver):
    app = create_app()
    mock_server = init_mock_server(httpserver)

    app.config['TESTING'] = True
    app.config['GHIBLI_API_URL'] = mock_server.url_for('')

    return app


def init_mock_server(httpserver):
    json_films = [
        {
            "id": "123",
            "title": "mtest1",
            "release_date": "2313"
        },
        {
            "id": "321",
            "title": "mtest2",
            "release_date": "2313"
        }
    ]

    json_people = [
        {
            "id": "123",
            "name": "ptest1",
            "films": [
                f"{httpserver.url_for('/films')}/123",
            ]
        },
        {
            "id": "12341",
            "name": "ptest2",
            "films": [
                f"{httpserver.url_for('/films')}/321",
            ]
        }
    ]

    httpserver.expect_request(
        "/films"
    ).respond_with_json(json_films, status=200)

    httpserver.expect_request(
        "/people"
    ).respond_with_json(json_people, status=200)

    return httpserver
