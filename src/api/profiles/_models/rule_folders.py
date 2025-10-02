from dataclasses import dataclass

from api.profiles.constants import Do, Status


@dataclass
class ListActionItem:
    do: Do
    status: Status

    def __init__(self, do: Do, status: Status):
        self.do = Do(do)
        self.status = Status(status)


@dataclass
class CreateActionItems(ListActionItem):
    via: str

    def __init__(self, do: Do, status: Status, via: str):
        super().__init__(do, status)
        self.via = via


@dataclass
class ListRuleFolderItem:
    PK: int
    group: str
    action: ListActionItem
    count: int

    def __init__(self, PK: int, group: str, action: dict, count: int):
        self.PK = PK
        self.group = group
        self.action = ListActionItem(action["do"], action["status"])
        self.count = count


@dataclass
class CreateRuleFolderItem:
    PK: int
    group: str
    action: CreateActionItems
    count: int

    def __init__(self, PK: int, group: str, action: dict, count: int):
        self.PK = PK
        self.group = group
        self.action = CreateActionItems(action["do"], action["status"], action["via"])
        self.count = count
