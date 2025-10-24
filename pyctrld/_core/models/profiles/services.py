from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import Action, ProfilesBaseModel


class Service(ProfilesBaseModel):
    PK: str
    name: str
    unlock_location: str
    warning: Optional[str] = None
    category: str
    action: Action
