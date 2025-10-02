from dataclasses import dataclass
from typing import List, Optional

from api.profiles._base import ActionItem
from api.profiles.constants import Do, Status


@dataclass
class ServiceItem:
    """ServiceItem dataclass definition for service data from the API."""

    PK: str
    name: str
    locations: List[str]
    unlock_location: str
    warning: Optional[str]
    category: str
    action: ActionItem

    def __init__(self, **kwargs):
        self.PK = kwargs["PK"]
        self.name = kwargs["name"]
        self.locations = kwargs["locations"]
        self.unlock_location = kwargs["unlock_location"]
        self.warning = kwargs.get("warning")
        self.category = kwargs["category"]

        action = kwargs["action"]
        self.action = ActionItem(do=action["do"], status=action["status"], via=action.get("via"))


@dataclass
class ServiceModifedItem:
    do: Optional[Do]
    via: Optional[str]
    status: Optional[Status]

    def __init__(
        self, do: Optional[Do] = None, via: Optional[str] = None, status: Optional[Status] = None
    ):
        self.do = None if do is None else Do(do)
        self.via = via
        self.status = None if status is None else Status(status)
