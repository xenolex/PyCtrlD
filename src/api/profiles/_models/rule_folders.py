from pydantic import field_validator, model_validator

from api.profiles._base import ConfiguratedBaseModel
from api.profiles.constants import Do, Status


class ListActionItem(ConfiguratedBaseModel):
    do: Do
    status: Status

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


class CreateActionItems(ListActionItem):
    via: str


class ListRuleFolderItem(ConfiguratedBaseModel):
    PK: int
    group: str
    action: ListActionItem
    count: int

    @model_validator(mode="before")
    @classmethod
    def validate_list_rule_folder_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = ListActionItem(do=action_dict["do"], status=action_dict["status"])
        return values


class CreateRuleFolderItem(ConfiguratedBaseModel):
    PK: int
    group: str
    action: CreateActionItems
    count: int

    @model_validator(mode="before")
    @classmethod
    def validate_create_rule_folder_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = CreateActionItems(
                do=action_dict["do"], status=action_dict["status"], via=action_dict["via"]
            )
        return values
