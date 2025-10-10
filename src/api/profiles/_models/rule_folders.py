from pydantic import model_validator

from api._base import ConfiguratedBaseModel
from api.profiles._base import Action


class RuleFolder(ConfiguratedBaseModel):
    PK: int
    group: str
    action: Action
    count: int

    @model_validator(mode="before")
    @classmethod
    def validate_list_rule_folder_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = Action.model_validate(action_dict, strict=True)
        return values
