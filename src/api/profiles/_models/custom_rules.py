from dataclasses import dataclass
from typing import Optional

from api.profiles._models.services import ActionItem
from api.profiles.constants import Do, Status


@dataclass
class ListCustomRuleItem:
    PK: str
    order: int
    group: int
    action: ActionItem

    def __init__(self, PK: str, order: int, group: int, action: dict):
        self.PK = PK
        self.order = order
        self.group = group
        self.action = ActionItem(do=action["do"], status=action["status"], via=action.get("via"))


@dataclass
class CreateCustomRuleItem:
    do: Optional[Do]
    status: Optional[Status]
    via: Optional[str]
    order: Optional[int]
    group: Optional[int]

    def __init__(
        self,
        do: Optional[Do] = None,
        status: Optional[Status] = None,
        via: Optional[str] = None,
        order: Optional[int] = None,
        group: Optional[int] = None,
    ):
        self.do = None if do is None else Do(do)
        self.status = None if status is None else Status(status)
        self.via = via
        self.order = order
        self.group = group
