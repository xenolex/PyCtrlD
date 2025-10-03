from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from api.profiles._base import ActionItem
from api.profiles.constants import Do, Status


class CustomRulesActionItem(ActionItem):
    via_v6: Optional[str] = None  # not documented


class ListCustomRuleItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    PK: str
    order: int
    group: int
    action: CustomRulesActionItem
    comment: Optional[str] = None  # not documented

    @model_validator(mode="before")
    @classmethod
    def validate_list_custom_rule_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = CustomRulesActionItem.model_validate(action_dict, strict=True)
        return values


class CreatedCustomRuleItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    do: Do
    status: Status
    via: Optional[str] = None
    via_v6: Optional[str] = None  # Not documented
    order: Optional[int] = None
    group: Optional[int] = None

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)
