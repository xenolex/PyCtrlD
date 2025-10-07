from typing import List

from pydantic import field_validator, model_validator

from api.profiles._base import ConfiguratedBaseModel, Do, Status, create_list_of_items


class LevelItem(ConfiguratedBaseModel):
    type: str
    name: str
    status: Status
    title: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


class FilterItem(ConfiguratedBaseModel):
    """FilterItem Pydantic model definition"""

    PK: str
    name: str
    description: str
    additional: str
    sources: List[str]
    options: List[LevelItem]

    @model_validator(mode="before")
    @classmethod
    def validate_filter_item(cls, values):
        if isinstance(values, dict) and "options" in values and isinstance(values["options"], list):
            # Convert dict options to OptionItem instances
            option_items = []
            for option in values["options"]:
                option_items.append(LevelItem.model_validate(option, strict=True))
            values["options"] = option_items
        return values


class NativeActionItem(ConfiguratedBaseModel):
    do: Do
    lvl: str
    status: Status

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


class NativeFilterItem(ConfiguratedBaseModel):
    """FilterItem Pydantic model definition"""

    PK: str
    action: NativeActionItem
    additional: str
    description: str
    levels: List[LevelItem]
    name: str
    sources: List[str]
    status: Status

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, v):
        return NativeActionItem.model_validate(v, strict=True)

    @model_validator(mode="before")
    @classmethod
    def validate_level(cls, values):
        return create_list_of_items(model=LevelItem, items=values["levels"])
