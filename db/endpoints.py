from db_client import database

def insert_endpoint(collection_id: int, name: str, url: str):
    database.execute(
        "INSERT INTO endpoints (collection_id, name, url) VALUES (?, ?, ?)",
        (collection_id, name, url),
    )
    database.commit()

def get_endpoints(collection_id: int):
    cursor = database.execute(
        "SELECT id, collection_id, name, url, created_at, updated_at "
        "FROM endpoints WHERE collection_id = ? ORDER BY name",
        (collection_id,),
    )
    return cursor.fetchall()

def get_endpoint(endpoint_id: int):
    cursor = database.execute(
        "SELECT id, collection_id, name, url, created_at, updated_at "
        "FROM endpoints WHERE id = ?",
        (endpoint_id,),
    )
    return cursor.fetchone()

def update_endpoint(endpoint_id: int, name: str, url: str):
    database.execute(
        "UPDATE endpoints SET name = ?, url = ?, updated_at = CURRENT_TIMESTAMP "
        "WHERE id = ?",
        (name, url, endpoint_id),
    )
    database.commit()

def delete_endpoint(endpoint_id: int):
    database.execute("DELETE FROM endpoints WHERE id = ?", (endpoint_id,))
    database.commit()
