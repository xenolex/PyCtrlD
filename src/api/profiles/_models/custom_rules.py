from typing import Optional

from pydantic import field_validator, model_validator

from api._core import ConfiguratedBaseModel
from api.profiles._base import Action
from api.profiles.constants import Do, Status


class CustomRule(ConfiguratedBaseModel):
    PK: str
    order: int
    group: int
    action: Action
    comment: Optional[str] = None  # not documented

    @model_validator(mode="before")
    @classmethod
    def validate_list_custom_rule_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = Action.model_validate(action_dict, strict=True)
        return values


class ModifiedCustomRule(ConfiguratedBaseModel):
    do: Do
    status: Status
    order: int
    group: int
    via: Optional[str] = None
    via_v6: Optional[str] = None  # Not documented

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)
