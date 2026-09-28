from components.tabs.keyvalue import KeyValueEditor


class RequestParams(KeyValueEditor):
    def __init__(self) -> None:
        super().__init__(prefix="request-params")
