#Tables

COLLECTIONS = """CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


ENDPOINTS = """CREATE TABLE IF NOT EXISTS endpoints (
    id INTEGER PRIMARY KEY,
    collection_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (collection_id)
        REFERENCES collections(id)
        ON DELETE CASCADE
);"""

REQUESTS = """CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY,
    endpoint_id INTEGER NOT NULL,
    method TEXT NOT NULL,
    headers JSON,
    cookies JSON,
    params JSON,
    authorization JSON,
    body TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (endpoint_id)
        REFERENCES endpoints(id)
        ON DELETE CASCADE
);"""

RESPONSES = """CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY,
    request_id INTEGER NOT NULL,
    status_code INTEGER,
    delay INTEGER,
    headers JSON,
    body TEXT,
    cookies JSON,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (request_id)
        REFERENCES requests(id)
        ON DELETE CASCADE
);"""


