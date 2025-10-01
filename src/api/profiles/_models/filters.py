from dataclasses import dataclass
from typing import List


@dataclass
class OptionItem:
    title: str
    description: str
    type: str
    name: str
    status: int


@dataclass
class FilterItem:
    """FilterItem dataclass definition"""

    PK: str
    name: str
    description: str
    additional: str
    sources: List[str]
    options: List[OptionItem]

    def __init__(
        self,
        PK: str,
        name: str,
        description: str,
        additional: str,
        sources: List[str],
        options: List[dict],
    ):
        self.PK = PK
        self.name = name
        self.description = description
        self.additional = additional
        self.sources = sources

        self.options = [
            OptionItem(
                title=option["title"],
                description=option["description"],
                type=option["type"],
                name=option["name"],
                status=option["status"],
            )
            for option in options
        ]
