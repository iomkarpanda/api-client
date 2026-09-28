from db.collections import get_collections, insert_collection
from db.endpoints import get_endpoints, insert_endpoint
from db.requests import insert_request

SAMPLES = [
    {
        "collection": "JSONPlaceholder",
        "endpoints": [
            {
                "name": "List posts",
                "url": "https://jsonplaceholder.typicode.com/posts",
                "request": {
                    "method": "get",
                    "headers": {"Accept": "application/json"},
                    "params": {"userId": "1", "_limit": "10"},
                },
            },
            {
                "name": "Get post",
                "url": "https://jsonplaceholder.typicode.com/posts/1",
                "request": {
                    "method": "get",
                    "headers": {"Accept": "application/json"},
                },
            },
            {
                "name": "Create post",
                "url": "https://jsonplaceholder.typicode.com/posts",
                "request": {
                    "method": "post",
                    "headers": {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    "body": (
                        "{\n"
                        '  "title": "sample post",\n'
                        '  "body": "created by seed.py",\n'
                        '  "userId": 1\n'
                        "}"
                    ),
                },
            },
        ],
    },
    {
        "collection": "GitHub API",
        "endpoints": [
            {
                "name": "Get user",
                "url": "https://api.github.com/users/octocat",
                "request": {
                    "method": "get",
                    "headers": {
                        "Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2022-11-28",
                    },
                    "authorization": {"type": "bearer", "token": "ghp_sample_token"},
                },
            },
            {
                "name": "Search repositories",
                "url": "https://api.github.com/search/repositories",
                "request": {
                    "method": "get",
                    "headers": {"Accept": "application/vnd.github+json"},
                    "params": {"q": "textual", "sort": "stars", "order": "desc"},
                },
            },
        ],
    },
    {
        "collection": "HTTPBin",
        "endpoints": [
            {
                "name": "Inspect headers",
                "url": "https://httpbin.org/headers",
                "request": {
                    "method": "get",
                    "headers": {"X-Demo": "api-client"},
                },
            },
            {
                "name": "Inspect cookies",
                "url": "https://httpbin.org/cookies",
                "request": {
                    "method": "get",
                    "cookies": {"session_id": "abc123def456", "theme": "dark"},
                },
            },
            {
                "name": "Basic auth",
                "url": "https://httpbin.org/basic-auth/user/passwd",
                "request": {
                    "method": "get",
                    "authorization": {"type": "basic", "username": "user", "password": "passwd"},
                },
            },
        ],
    },
]


def seed() -> None:
    existing = {name for _, name, _, _ in get_collections()}

    for sample in SAMPLES:
        name = sample["collection"]

        if name in existing:
            print(f"skipped {name} (already exists)")
            continue

        insert_collection(name)
        collection_id = next(
            cid for cid, cname, _, _ in get_collections() if cname == name
        )

        for endpoint in sample["endpoints"]:
            insert_endpoint(collection_id, endpoint["name"], endpoint["url"])
            endpoint_id = next(
                ep[0] for ep in get_endpoints(collection_id) if ep[2] == endpoint["name"]
            )
            insert_request(endpoint_id, **endpoint["request"])

        print(f"seeded {name} ({len(sample['endpoints'])} endpoints)")

    total_endpoints = sum(len(s["endpoints"]) for s in SAMPLES)
    print(f"done: {len(SAMPLES)} sample collections, {total_endpoints} endpoints")


if __name__ == "__main__":
    seed()
