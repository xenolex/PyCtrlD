from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import Action, ConfiguratedBaseModel, Do, ProfilesBaseModel, Status


class CustomRule(ProfilesBaseModel):
    PK: str
    order: int
    group: int
    action: Action
    comment: Optional[str] = None  # not documented


class ModifiedCustomRule(ConfiguratedBaseModel):
    do: Do
    status: Status
    order: int
    group: int
    via: Optional[str] = None
    via_v6: Optional[str] = None  # Not documented
