from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator

from api.profiles._base import ActionItem
from api.profiles.constants import Do, Status


class ServiceItem(BaseModel):
    PK: str
    name: str
    locations: List[str]
    unlock_location: str
    warning: Optional[str] = None
    category: str
    action: ActionItem

    @model_validator(mode="before")
    @classmethod
    def validate_service_item(cls, values):
        if isinstance(values, dict) and "action" in values and isinstance(values["action"], dict):
            action_dict = values["action"]
            values["action"] = ActionItem(
                do=action_dict["do"], status=action_dict["status"], via=action_dict.get("via")
            )
        return values


class ServiceModifedItem(BaseModel):
    do: Optional[Do] = None
    via: Optional[str] = None
    status: Optional[Status] = None

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return None if v is None else Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return None if v is None else Status(v)
