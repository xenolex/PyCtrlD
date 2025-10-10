from typing import Optional

from pydantic import model_validator

from api._base import ConfiguratedBaseModel
from api.profiles._base import Action


class Service(ConfiguratedBaseModel):
    PK: str
    name: str
    unlock_location: str
    warning: Optional[str] = None
    category: str
    action: Action

    @model_validator(mode="before")
    @classmethod
    def validate_service_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = Action.model_validate(action_dict, strict=True)
        return values
