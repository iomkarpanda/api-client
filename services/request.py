import json

import requests


def make_request(url: str) -> requests.Response:
    return requests.get(url, timeout=10)


def parse_response(response: requests.Response) -> str:
    try:
        body = json.dumps(response.json(), indent=2)
    except ValueError:
        body = response.text

    headers = "\n".join(
        f"{name}: {value}" for name, value in response.headers.items()
    )
    return (
        f"Status: {response.status_code} {response.reason}\n\n"
        f"Headers:\n{headers}\n\n"
        f"Body:\n{body}"
    )