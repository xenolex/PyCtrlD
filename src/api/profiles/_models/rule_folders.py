from pydantic import model_validator

from api.profiles._base import ActionItem, ConfiguratedBaseModel


class RuleFolderItem(ConfiguratedBaseModel):
    PK: int
    group: str
    action: ActionItem
    count: int

    @model_validator(mode="before")
    @classmethod
    def validate_list_rule_folder_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = ActionItem.model_validate(action_dict, strict=True)
        return values
