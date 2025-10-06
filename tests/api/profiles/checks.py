from pprint import pprint
from typing import Any, Dict, Optional

from pydantic import BaseModel


def check_key_in_model(key: str, model: type[BaseModel]) -> None:
    assert key in model.model_fields, f"Key '{key}' not found in '{model.__name__}' class"


def check_api_list_endpoint(
    api: Any, model: type[BaseModel], api_kwargs: Optional[Dict[str, Any]] = None
):
    if api_kwargs is None:
        api_kwargs = {}
    items = api.list(**api_kwargs)
    for item in items:
        pprint(item)
        assert isinstance(item, model), f"Api returns items is not an instance of {model.__name__}"
