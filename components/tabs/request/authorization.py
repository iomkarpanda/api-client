from components.tabs.keyvalue import KeyValueEditor


class Authorization(KeyValueEditor):
    def __init__(self) -> None:
        super().__init__(prefix="request-authorization")
