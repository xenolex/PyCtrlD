from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from api._core.logger import logger


def check_key_in_model(key: str, model: type[BaseModel]) -> None:
    assert key in model.model_fields, f"Key '{key}' not found in '{model.__name__}' class"


if TYPE_CHECKING:
    from typing import Any, Optional


def check_api_list_endpoint(
    api: Any,
    model: type[BaseModel],
    api_kwargs: Optional[dict[str, Any]] = None,
    method_name="list",
):
    if api_kwargs is None:
        api_kwargs = {}
    func = getattr(api, method_name)
    items = func(**api_kwargs)

    for item in items:
        logger.info(item)
        assert isinstance(item, model), f"Api returns items is not an instance of {model.__name__}"
