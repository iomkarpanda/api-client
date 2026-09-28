from components.tabs.keyvalue import KeyValueEditor


class RequestHeader(KeyValueEditor):
    def __init__(self) -> None:
        super().__init__(prefix="request-headers")
