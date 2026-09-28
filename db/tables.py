from db.db_client import database
from db.sql import COLLECTIONS, ENDPOINTS, REQUESTS, RESPONSES


def create_collections():
    database.execute(COLLECTIONS)
    database.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_collections_name "
        "ON collections(name)"
    )


def create_endpoints():
    database.execute(ENDPOINTS)


def create_requests():
    database.execute(REQUESTS)


def create_responses():
    database.execute(RESPONSES)


def create_tables():
    create_collections()
    create_endpoints()
    create_requests()
    create_responses()
    database.commit()
