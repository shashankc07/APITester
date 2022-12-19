import requests

resource = "/DecisionService/rest/Miniloan/1.0/my_operation/1.3/WADL"


def test_payload(endpoint, payload):
    req = requests.get(endpoint+resource, params=payload)
    return req.text


def test_url(endpoint):
    req = requests.get(endpoint)
    return req.status_code


