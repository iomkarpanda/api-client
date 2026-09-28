import json

from db.db_client import database


def _encode_json(value):
    if value is None:
        return None
    return json.dumps(value)


def _decode_response(row):
    if row is None:
        return None

    values = list(row)
    for index in (4, 6):
        if values[index] is not None:
            values[index] = json.loads(values[index])
    return tuple(values)

def insert_response(
    request_id: int,
    status_code: int | None = None,
    delay: int | None = None,
    headers: object | None = None,
    body: str | None = None,
    cookies: object | None = None,
):
    database.execute(
        "INSERT INTO responses "
        "(request_id, status_code, delay, headers, body, cookies) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (request_id, status_code, delay, _encode_json(headers), body, _encode_json(cookies)),
    )
    database.commit()

def get_responses(request_id: int):
    cursor = database.execute(
        "SELECT id, request_id, status_code, delay, headers, body, cookies, "
        "created_at, updated_at "
        "FROM responses WHERE request_id = ? ORDER BY id",
        (request_id,),
    )
    return [_decode_response(row) for row in cursor.fetchall()]

def get_response(response_id: int):
    cursor = database.execute(
        "SELECT id, request_id, status_code, delay, headers, body, cookies, "
        "created_at, updated_at "
        "FROM responses WHERE id = ?",
        (response_id,),
    )
    return _decode_response(cursor.fetchone())

def update_response(
    response_id: int,
    status_code: int | None = None,
    delay: int | None = None,
    headers: object | None = None,
    body: str | None = None,
    cookies: object | None = None,
):
    database.execute(
        "UPDATE responses SET status_code = ?, delay = ?, headers = ?, "
        "body = ?, cookies = ?, updated_at = CURRENT_TIMESTAMP "
        "WHERE id = ?",
        (status_code, delay, _encode_json(headers), body, _encode_json(cookies), response_id),
    )
    database.commit()

def delete_response(response_id: int):
    database.execute("DELETE FROM responses WHERE id = ?", (response_id,))
    database.commit()
