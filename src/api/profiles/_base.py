import requests


class BaseApi:
    def __init__(self, token: str) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {token}", "accept": "application/json"}
        )
        self._url = "https://api.controld.com/profiles"
