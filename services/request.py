import json

import requests


def _authorization(authorization: object | None) -> tuple[dict, object | None]:
    if not isinstance(authorization, dict):
        return {}, None

    kind = str(authorization.get("type", "")).lower()
    if kind == "bearer" and authorization.get("token"):
        return {"Authorization": f"Bearer {authorization['token']}"}, None
    if kind == "basic":
        username = authorization.get("username", "")
        password = authorization.get("password", "")
        return {}, requests.auth.HTTPBasicAuth(username, password)
    return {}, None


def make_request(
    url: str,
    method: str = "get",
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    auth_headers, auth = _authorization(authorization)

    request_headers = {**(headers or {}), **auth_headers}
    kwargs = {"timeout": timeout}
    if request_headers:
        kwargs["headers"] = request_headers
    if params:
        kwargs["params"] = params
    if cookies:
        kwargs["cookies"] = cookies
    if auth is not None:
        kwargs["auth"] = auth
    if body:
        kwargs["data"] = body

    return requests.request(method.upper(), url, **kwargs)


def get(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    return make_request(
        url,
        method="get",
        headers=headers,
        params=params,
        cookies=cookies,
        authorization=authorization,
        body=body,
        timeout=timeout,
    )


def post(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    return make_request(
        url,
        method="post",
        headers=headers,
        params=params,
        cookies=cookies,
        authorization=authorization,
        body=body,
        timeout=timeout,
    )


def put(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    return make_request(
        url,
        method="put",
        headers=headers,
        params=params,
        cookies=cookies,
        authorization=authorization,
        body=body,
        timeout=timeout,
    )


def patch(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    return make_request(
        url,
        method="patch",
        headers=headers,
        params=params,
        cookies=cookies,
        authorization=authorization,
        body=body,
        timeout=timeout,
    )


def delete(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    return make_request(
        url,
        method="delete",
        headers=headers,
        params=params,
        cookies=cookies,
        authorization=authorization,
        body=body,
        timeout=timeout,
    )


def options(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
    cookies: dict | None = None,
    authorization: object | None = None,
    body: str | None = None,
    timeout: int = 10,
) -> requests.Response:
    return make_request(
        url,
        method="options",
        headers=headers,
        params=params,
        cookies=cookies,
        authorization=authorization,
        body=body,
        timeout=timeout,
    )


METHODS = {
    "get": get,
    "post": post,
    "put": put,
    "patch": patch,
    "delete": delete,
    "options": options,
}


def response_delay(response: requests.Response) -> int:
    return int(response.elapsed.total_seconds() * 1000)


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
