from app.tools.requests import get_json


requests = [
    {
        "request": "/",
        "response": {
            "code": 200,
            "data": {'field1': 'value1', 'field2': 'value2'}
        }
    },
    {
        "request": "/random",
        "response": {
            "code": 200,
            "data": {'field1': 'value1', 'field2': 'value2'}
        }
    },
    {
        "request": "/error",
        "response": {
            "code": 404,
            "data": "Data not found"
        }
    },
]


def test_get_json(httpserver):
    for r in requests:
        httpserver.expect_request(
            r["request"]
        ).respond_with_json(r["response"]["data"],
                            status=r["response"]["code"])

        resp = get_json(httpserver.url_for(r["request"]))
        assert resp.status_code == r["response"]["code"]
        assert resp.json() == r["response"]["data"]
