from pydantic import BaseModel


def check_key_model(key: str, model: type[BaseModel]) -> None:
    assert key in model.model_fields, f"Key '{key}' not found in '{model.__name__}' class"
