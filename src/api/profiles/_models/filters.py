from typing import List

from pydantic import BaseModel, model_validator


class OptionItem(BaseModel):
    title: str
    description: str
    type: str
    name: str
    status: int


class FilterItem(BaseModel):
    """FilterItem Pydantic model definition"""

    PK: str
    name: str
    description: str
    additional: str
    sources: List[str]
    options: List[OptionItem]

    @model_validator(mode="before")
    @classmethod
    def validate_filter_item(cls, values):
        if isinstance(values, dict) and "options" in values and isinstance(values["options"], list):
            # Convert dict options to OptionItem instances
            option_items = []
            for option in values["options"]:
                if isinstance(option, dict):
                    option_items.append(
                        OptionItem(
                            title=option["title"],
                            description=option["description"],
                            type=option["type"],
                            name=option["name"],
                            status=option["status"],
                        )
                    )
                else:
                    option_items.append(option)
            values["options"] = option_items
        return values
