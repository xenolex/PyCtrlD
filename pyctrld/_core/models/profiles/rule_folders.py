from __future__ import annotations

from pyctrld._core.models.common import Action, ProfilesBaseModel


class RuleFolder(ProfilesBaseModel):
    PK: int
    group: str
    action: Action
    count: int
