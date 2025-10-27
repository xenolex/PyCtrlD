"""Account models for ControlD API.

This module provides data models for user account information including
status, settings, and authentication details.
"""

from __future__ import annotations

from typing import Any

from pyctrld._core.models.common import ConfiguratedBaseModel, Status


class UserData(ConfiguratedBaseModel):
    """User account data model.

    Represents detailed information about a ControlD user account including
    status, authentication settings, and configuration.

    Attributes:
        last_active: Timestamp of last account activity.
        proxy_access: Proxy access level for the account.
        email_status: Email verification status.
        status: Account status (enabled/disabled).
        email: User's email address.
        date: Account creation date.
        PK: Primary key (unique identifier) for the user.
        twofa: Two-factor authentication status.
        v: Version number.
        sso: Single sign-on provider identifier.
        stats_endpoint: Analytics/statistics endpoint URL.
        debug: Debug information and flags.
    """

    last_active: int
    proxy_access: int
    email_status: int
    status: Status
    email: str
    date: str
    PK: str
    twofa: int
    v: int
    sso: str
    stats_endpoint: str
    debug: list[Any]
