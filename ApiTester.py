import requests


def test_payload(url, payload):
    req = requests.get(url, params=payload)
    return req.text


def test_url(url):
    req = requests.get(url)
    assert req.status_code == 200


test_url('https://www.google.com')
