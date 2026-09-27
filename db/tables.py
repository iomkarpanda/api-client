from sql import COLLECTIONS,ENDPOINTS,REQUESTS,RESPONSES
from db_client import database

def create_collections():
    database.execute(COLLECTIONS)
    database.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_collections_name "
        "ON collections(name)"
    )
    database.commit()

def create_endpoints():
    database.execute(ENDPOINTS)

def create_requests():
    database.execute(REQUESTS)

def create_responses():
    database.execute(RESPONSES)

