from typing import Optional

from pydantic import field_validator, model_validator

from api.profiles._base import ConfiguratedBaseModel
from api.profiles.constants import Do, Status


class RuleFolderActionItem(ConfiguratedBaseModel):
    do: Optional[Do] = None
    status: Optional[Status] = None
    via: Optional[str] = None
    via_v6: Optional[str] = None

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        if v is None:
            return None
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return None
        return Status(v)


class RuleFolderItem(ConfiguratedBaseModel):
    PK: int
    group: str
    action: RuleFolderActionItem
    count: int

    @model_validator(mode="before")
    @classmethod
    def validate_list_rule_folder_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = RuleFolderActionItem.model_validate(action_dict, strict=True)
        return values
