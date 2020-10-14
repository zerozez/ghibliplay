import pytest

from app.views.movies.index import get_fimls, get_cast

from app.tools.requests import InvalidResponse


def test_movie_index(client):
    resp = client.get('/movies')
    assert resp.status_code == 308

    resp = client.get('/movies/')

    assert resp.status_code == 200
    assert b"mtest1" in resp.data
    assert b"mtest2" in resp.data
    assert b"ptest1" in resp.data
    assert b"ptest2" in resp.data


def test_get_films(httpserver):
    # Making valid request
    json = [{
        "id": "123",
        "title": "test1",
        "release_date": "2313"
    }]
    httpserver.expect_request(
        "/films"
    ).respond_with_json(json, status=200)

    resp = get_fimls(httpserver.url_for(""))
    assert resp == json

    httpserver.clear()
    httpserver.expect_request(
        "/films"
    ).respond_with_json("No data", status=404)

    with pytest.raises(InvalidResponse) as exinfo:
        get_fimls(httpserver.url_for(""))

    assert "404" in str(exinfo.value)
    assert "No data" in str(exinfo.value)


def test_get_cast(httpserver):
    json = [
        {
            "id": "23-c0912m3c",
            "name": "v1",
            "films": [
                f"{httpserver.url_for('/films')}/12c0m912-39m",
                f"{httpserver.url_for('/films')}/12938cm12-123"
            ]
        },
        {
            "id": "2dfdf3c",
            "name": "v2",
            "films": [
                f"{httpserver.url_for('/films')}/12938cm12-123"
            ]
        }
    ]

    resp_cast = {
        "films": {
            "12938cm12-123": set([
                "23-c0912m3c",
                "2dfdf3c"
            ]),
            "12c0m912-39m": set([
                "23-c0912m3c"
            ]),
        },
        "people": {
            "23-c0912m3c": "v1",
            "2dfdf3c": "v2"
        }
    }

    httpserver.expect_request(
        "/people"
    ).respond_with_json(json, status=200)

    resp = get_cast(httpserver.url_for(""))
    assert resp == resp_cast
