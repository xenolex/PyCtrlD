"""Custom rules endpoint for ControlD API.

This module provides functionality for managing custom DNS filtering rules
within profiles, including creating, modifying, deleting, and listing rules.
"""

from __future__ import annotations

from typing import Optional

from pydantic import field_validator, model_validator

from pyctrld._core.logger import logger
from pyctrld._core.models.common import BaseFormData, Do, Status
from pyctrld._core.models.profiles.custom_rules import (
    CustomRule,
    ModifiedCustomRule,
)
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import (
    BaseEndpoint,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
)


class __BaseCustomRuleFormData(BaseFormData):
    """Base form data class for custom rule operations.

    This is an internal base class that provides common fields and validation
    for both creating and modifying custom rules.

    Attributes:
        via: Spoof/Redirect target. For SPOOF: IPv4 or hostname. For REDIRECT: proxy identifier.
        via_v6: IPv6 address (AAAA record) when using SPOOF action.
        group: Group/folder ID to organize rules.
        hostnames: List of hostnames this rule applies to.
    """

    via: Optional[str] = None
    via_v6: Optional[str] = None
    group: Optional[int] = None
    hostnames: list[str]

    @model_validator(mode="after")
    def validate_rule_constraints(self) -> __BaseCustomRuleFormData:
        """Validate rule constraints based on the action type.

        Returns:
            Self reference after validation.

        Raises:
            ValueError: If validation constraints are not met.
        """
        do = getattr(self, "do", None)
        if do == Do.SPOOF:
            check_via_is_record_or_cname(self.via)
            check_via_v6_is_aaaa_record(self.via_v6)

        if do == Do.REDIRECT:
            check_via_is_proxy_identifier(self.via)
            if self.via_v6 is not None:
                logger.warning('"via_v6" has no effect for REDIRECT')

        return self


class CreateCustomRuleFormData(__BaseCustomRuleFormData):
    """Form data for creating custom rules.

    Args:
        do (int | Do): Rule type. (BLOCK = 0, BYPASS = 1, SPOOF = 2, REDIRECT = 3).
        status (bool): Rule status. (ENABLED or DISABLED).
        via (Optional[str]): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                   If REDIRECT, this must be a valid proxy identifier.
        via_v6 (Optional[str]): If SPOOF this can be a valid IPv6 address (AAAA record).
        group (Optional[int]): Group ID to organize rules.
        hostnames (list[str]): list of hostnames this rule applies to. len(hostnames) rules will be created
    """

    do: Do | int
    status: bool | Status

    @field_validator("do", mode="before")
    @classmethod
    def set_do(cls, value):
        return Do(value)


class ModifyCustomRuleFormData(__BaseCustomRuleFormData):
    """Form data modifying custom rules.

    Args:
        do (Optional[Do | int]):  Rule type. (BLOCK = 0, BYPASS = 1, SPOOF = 2, REDIRECT = 3).
        status (Optional[bool]): Rule status. (ENABLED or DISABLED).
        via (str): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                   If REDIRECT, this must be a valid proxy identifier.
        via_v6 (Optional[str]): If SPOOF this can be a valid IPv6 address (AAAA record).
        group (int): Group ID to organize rules.
        hostnames (list[str]): list of hostnames this rule applies to. len(hostnames) rules will be created
    """

    do: Optional[Do | int] = None
    status: Optional[bool | Status] = None

    @field_validator("do", mode="before")
    @classmethod
    def set_do(cls, value):
        return None if value is None else Do(value)


class CustomRulesEndpoint(BaseEndpoint):
    """Endpoint for managing custom DNS filtering rules.

    This endpoint provides methods to create, list, modify, and delete custom
    DNS rules within a profile. Rules can be organized into folders/groups.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the CustomRules endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.CUSTOM_RULES

    def list(self, profile_id: str, folder_id: Optional[int] = None) -> list[CustomRule]:
        """Return custom rules in a folder.

        Lists all custom DNS rules within the specified folder of a profile.
        For root folder, omit the folder_id parameter.

        Args:
            profile_id: Primary key (PK) of the profile.
            folder_id: Folder ID to list rules from. None for root folder.

        Returns:
            A list of CustomRule objects.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-rules-folder-id
        """
        url = self._url.format(profile_id=profile_id)
        url += f"/{'' if folder_id is None else folder_id}"

        return self._list(url=url, model=CustomRule, key="rules")

    def modify(
        self, profile_id: str, form_data: ModifyCustomRuleFormData
    ) -> list[ModifiedCustomRule]:
        """Modify existing custom rules.

        Updates one or more custom DNS rules based on the hostnames provided
        in the form data.

        Args:
            profile_id: Primary key (PK) of the profile.
            form_data: Form data containing hostnames and fields to update.

        Returns:
            A list of ModifiedCustomRule objects representing updated rules.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-rules
        """
        url = self._url.format(profile_id=profile_id)
        return self._modify(
            url=url, model=ModifiedCustomRule, key="rules", form_data=form_data.model_dump_json()
        )

    def create(
        self, profile_id: str, form_data: CreateCustomRuleFormData
    ) -> list[ModifiedCustomRule]:
        """Create one or more custom rules.

        Creates custom DNS rules for each hostname provided in the form data.
        The number of rules created equals the length of the hostnames list.

        Args:
            profile_id: Primary key (PK) of the profile.
            form_data: Form data containing rule configuration and hostnames.

        Returns:
            A list of ModifiedCustomRule objects representing created rules.

        Reference:
            https://docs.controld.com/reference/post_profiles-profile-id-rules
        """
        url = self._url.format(profile_id=profile_id)
        return self._create(
            url=url, model=ModifiedCustomRule, key="rules", form_data=form_data.model_dump_json()
        )

    def delete(self, profile_id: str, hostname: str) -> bool:
        """Delete custom rules for a specific hostname.

        Deletes all custom DNS rules associated with the specified hostname
        from the profile.

        Args:
            profile_id: Primary key (PK) of the profile.
            hostname: Hostname whose rules should be deleted.

        Returns:
            True if rules were deleted successfully.

        Reference:
            https://docs.controld.com/reference/delete_profiles-profile-id-rules-hostname
        """
        url = self._url.format(profile_id=profile_id) + f"/{hostname}"
        self._delete(url)
        return True
