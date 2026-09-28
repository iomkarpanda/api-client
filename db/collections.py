from db.db_client import database

def insert_collection(collection_name:str):
    database.execute(
        "INSERT INTO collections (name) VALUES (?)",
        (collection_name,),
    )
    database.commit()

def change_collection_name(old_collection_name: str, new_collection_name: str):

    cursor = database.execute(
        "SELECT id FROM collections WHERE name = ?",
        (old_collection_name,),
    )

    row = cursor.fetchone()

    if row is None:
        print("Collection not found")
        return

    collection_id = row[0]

    database.execute(
        "UPDATE collections SET name = ? WHERE id = ?",
        (new_collection_name, collection_id),
    )

    database.commit()


def get_collections():
    cursor = database.execute(
        "SELECT id, name, created_at, updated_at FROM collections ORDER BY name"
    )
    return cursor.fetchall()

def delete_collection(collection_name: str):
    database.execute(
        "DELETE FROM collections WHERE name = ?",
        (collection_name,),
    )
    database.commit()

