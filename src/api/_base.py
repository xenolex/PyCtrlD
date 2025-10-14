from typing import Any, Iterable, List

from pydantic import BaseModel, ConfigDict
from requests import Response, Session


class ConfiguratedBaseModel(BaseModel):
    """Base Pydantic model allowing unknown / extra fields."""

    model_config = ConfigDict(extra="allow")


class BaseEndpoint:
    def __init__(self, token: str) -> None:
        self._session = Session()

        self._session.headers.update(
            {"Authorization": f"Bearer {token}", "accept": "application/json"}
        )

        self._url = ""

    def __repr__(self):
        return f"<{self.__class__.__name__} url={self._url}>"

    def get_raw_response(self, url):
        return self._session.get(url)


def check_response(response: Response):
    class ApiError(Exception):
        def __init__(self, response: Response):
            data = response.json()["error"]

            message = (
                f"HTTP Status: {response.status_code} | "
                f"Error Code: {data['code']} | Message: {data['message']}"
            )

            super().__init__(message)

    if response.status_code != 200:
        raise ApiError(response)


def create_list_of_items(model: type, items: Iterable) -> List[Any]:
    """
    Validate an iterable of raw dict items into a list of model instances.

    The model is expected to expose a `model_validate` classmethod (e.g. Pydantic model).
    Strict validation is enforced to surface schema mismatches early.

    Args:
        model: The model class (e.g., a Pydantic BaseModel subclass) with model_validate.
        items: Iterable of raw item payloads (dict-like).

    Returns:
        List[Any]: List of validated model instances.
    """
    out_list: List[Any] = []
    for item in items:
        instance = model.model_validate(item, strict=True)  # type: ignore[attr-defined]
        out_list.append(instance)
    return out_list
