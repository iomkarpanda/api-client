import json

from db.db_client import database


def _encode_json(value):
    if value is None:
        return None
    return json.dumps(value)


def _decode_request(row):
    if row is None:
        return None

    values = list(row)
    for index in (3, 4, 5, 6):
        if values[index] is not None:
            values[index] = json.loads(values[index])
    return tuple(values)

def insert_request(
    endpoint_id: int,
    method: str,
    headers: object | None = None,
    cookies: object | None = None,
    params: object | None = None,
    authorization: object | None = None,
    body: str | None = None,
):
    cursor = database.execute(
        "INSERT INTO requests "
        "(endpoint_id, method, headers, cookies, params, authorization, body) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            endpoint_id,
            method,
            _encode_json(headers),
            _encode_json(cookies),
            _encode_json(params),
            _encode_json(authorization),
            body,
        ),
    )
    database.commit()
    return cursor.lastrowid

def get_requests(endpoint_id: int):
    cursor = database.execute(
        "SELECT id, endpoint_id, method, headers, cookies, params, "
        "authorization, body, created_at, updated_at "
        "FROM requests WHERE endpoint_id = ? ORDER BY id",
        (endpoint_id,),
    )
    return [_decode_request(row) for row in cursor.fetchall()]

def get_latest_request(endpoint_id: int):
    cursor = database.execute(
        "SELECT id, endpoint_id, method, headers, cookies, params, "
        "authorization, body, created_at, updated_at "
        "FROM requests WHERE endpoint_id = ? ORDER BY id DESC LIMIT 1",
        (endpoint_id,),
    )
    return _decode_request(cursor.fetchone())

def get_request(request_id: int):
    cursor = database.execute(
        "SELECT id, endpoint_id, method, headers, cookies, params, "
        "authorization, body, created_at, updated_at "
        "FROM requests WHERE id = ?",
        (request_id,),
    )
    return _decode_request(cursor.fetchone())

def update_request(
    request_id: int,
    method: str,
    headers: object | None = None,
    cookies: object | None = None,
    params: object | None = None,
    authorization: object | None = None,
    body: str | None = None,
):
    database.execute(
        "UPDATE requests SET method = ?, headers = ?, cookies = ?, params = ?, "
        "authorization = ?, body = ?, updated_at = CURRENT_TIMESTAMP "
        "WHERE id = ?",
        (
            method,
            _encode_json(headers),
            _encode_json(cookies),
            _encode_json(params),
            _encode_json(authorization),
            body,
            request_id,
        ),
    )
    database.commit()

def delete_request(request_id: int):
    database.execute("DELETE FROM requests WHERE id = ?", (request_id,))
    database.commit()
