"""Profile services models for ControlD API.

This module provides data models for service-based DNS filtering rules
within profiles.
"""

from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import Action, ProfilesBaseModel


class Service(ProfilesBaseModel):
    """Service-based DNS filtering rule model.

    Represents a service with its associated DNS filtering rule action
    configuration within a profile.

    Attributes:
        PK: Primary key (unique identifier) for the service.
        name: Service name.
        unlock_location: Location unlock information for the service.
        warning: Optional warning message about the service.
        category: Category identifier this service belongs to.
        action: Action configuration (do, status, via, via_v6).
    """

    PK: str
    name: str
    unlock_location: str
    warning: Optional[str] = None
    category: str
    action: Action
