# Terminal API Client

A keyboard-driven REST API client that runs entirely in your terminal. Built with Python and [Textual](https://textual.textualize.io/).

Think Postman — but fast, lightweight, and never leaves your terminal.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Textual](https://img.shields.io/badge/Textual-TUI-green) ![SQLite](https://img.shields.io/badge/SQLite-persistence-lightgrey)

---

## Features

- **Collections** — Organize endpoints into named collections with collapsible sidebar
- **Full request builder** — Params, Headers, Authorization (Bearer / Basic), Body, Cookies, Scripts, and Tests tabs
- **Response inspector** — Body, Preview, Headers, Cookies, Tests, and Timeline views with latency tracking
- **Request history** — Every response is persisted; revisit any past request from the timeline
- **Ad-hoc testing** — Fire off one-off requests without saving (Ctrl+O)
- **Keyboard-first UX** — Contextual key bindings, color-coded HTTP methods, custom dark theme
- **Local persistence** — All data stored in SQLite with foreign keys and cascade deletes

---

## Screenshot

```
┌─ Collections ──────────┬─ Request ─────────────────────────────────────────┐
│ ▸ JSONPlaceholder      │  Params  Headers  Auth  Body  Cookies  Scripts  Tests│
│ ▸ GitHub API           │  ┌──────────────────────────────────────────────┐  │
│ ▸ HTTPBin              │  │ Headers                                      │  │
│                        │  │ Accept: application/json                     │  │
│                        │  │                                              │  │
│                        │  └──────────────────────────────────────────────┘  │
│                        ├─ Response ─────────────────────────────────────────┤
│                        │  Body  Preview  Headers  Cookies  Tests  Timeline  │
│                        │  ┌──────────────────────────────────────────────┐  │
│                        │  │ {                                            │  │
│                        │  │   "userId": 1,                               │  │
│                        │  │   "id": 1,                                   │  │
│                        │  │   "title": "...",                            │  │
│                        │  │   "body": "..."                              │  │
│                        │  │ }                                            │  │
│                        │  └──────────────────────────────────────────────┘  │
└────────────────────────┴───────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- Python 3.12+

### Setup

```bash
git clone <repo-url>
cd api-client
pip install textual requests
```

---

## Usage

```bash
python main.py
```

On first run, the database is created automatically. To seed sample collections:

```bash
python seed.py
```

### Key Bindings

| Key       | Action                    |
|-----------|---------------------------|
| `Ctrl+O`  | Open ad-hoc test screen   |
| `Ctrl+S`  | Save current request      |
| `F2`      | Edit selected endpoint    |
| `Delete`  | Delete focused collection |
| `Escape`  | Close screen              |

---

## Project Structure

```
.
├── main.py                  # App entry point, layout, request orchestration
├── seed.py                  # Sample data seeder (JSONPlaceholder, GitHub, HTTPBin)
├── database.db              # SQLite database (auto-created)
│
├── components/              # UI widgets
│   ├── sidebar.py           # Collections sidebar with collapsible groups
│   ├── inputbar.py          # Method selector + URL input + Send/Save buttons
│   ├── request.py           # Request panel (tabbed config)
│   ├── response.py          # Response panel (tabbed viewer)
│   ├── tabbed.py            # TabbedContent with contextual help bar
│   └── tabs/
│       ├── request/         # Params, Headers, Auth, Body, Cookies, Scripts, Tests
│       └── response/        # Body, Preview, Headers, Cookies, Tests, Timeline
│
├── screens/                 # Modal screens
│   ├── edit_endpoint.py     # Edit endpoint name/URL
│   ├── save_request.py      # Save request to collection
│   ├── test.py              # Ad-hoc request tester
│   └── confirm.py           # Confirmation modal
│
├── db/                      # Persistence layer
│   ├── db_client.py         # SQLite connection
│   ├── sql.py               # Schema DDL
│   ├── tables.py            # Table creation
│   ├── collections.py       # Collection CRUD
│   ├── endpoints.py         # Endpoint CRUD
│   ├── requests.py          # Request CRUD (JSON encode/decode)
│   └── responses.py         # Response CRUD (JSON encode/decode)
│
└── services/
    └── request.py           # HTTP service (requests wrapper, auth, methods)
```

---

## Database Schema

```
collections ──1:N──> endpoints ──1:N──> requests ──1:N──> responses
```

| Table        | Key Fields                                                        |
|--------------|-------------------------------------------------------------------|
| `collections`| id, name (unique), created_at, updated_at                         |
| `endpoints`  | id, collection_id (FK), name, url, created_at, updated_at         |
| `requests`   | id, endpoint_id (FK), method, headers (JSON), cookies (JSON), params (JSON), authorization (JSON), body |
| `responses`  | id, request_id (FK), status_code, delay, headers (JSON), body, cookies (JSON) |

All foreign keys use `ON DELETE CASCADE`.

---

## Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Language   | Python 3.12         |
| TUI        | Textual             |
| HTTP       | requests            |
| Database   | SQLite 3            |
| Styling    | Rich (Text markup)  |

---

## License

MIT
