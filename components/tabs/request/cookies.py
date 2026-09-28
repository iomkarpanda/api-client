from components.tabs.keyvalue import KeyValueEditor


class RequestCookies(KeyValueEditor):
    def __init__(self) -> None:
        super().__init__(prefix="request-cookies")
