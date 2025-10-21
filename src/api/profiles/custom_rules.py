from __future__ import annotations

from typing import Optional

from pydantic import field_validator, model_validator

from api._core.models.common import BaseFormData, Do, Status
from api._core.models.profiles.custom_rules import (
    CustomRule,
    ModifiedCustomRule,
)
from api._core.urls import Endpoints
from api._core.utils import (
    BaseEndpoint,
    check_response,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
    create_list_of_items,
)


class __BaseCustomRuleFormData(BaseFormData):
    via: Optional[str] = None
    via_v6: Optional[str] = None
    group: Optional[int] = None
    hostnames: list[str]


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

    @model_validator(mode="after")
    def validate_rule_constraints(self):
        if self.do == Do.SPOOF:
            check_via_is_record_or_cname(self.via)
            check_via_v6_is_aaaa_record(self.via_v6)

        if self.do == Do.REDIRECT:
            check_via_is_proxy_identifier(self.via)
            if self.via_v6 is not None:
                # todo add logger
                # logger.warning("via_v6 has no effect for REDIRECT")
                print("via_v6 has no effect for REDIRECT")

        return self


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

    @model_validator(mode="after")
    def validate_rule_constraints(self):
        if self.do == Do.SPOOF:
            check_via_is_record_or_cname(self.via)
            check_via_v6_is_aaaa_record(self.via_v6)

        if self.do == Do.REDIRECT:
            check_via_is_proxy_identifier(self.via)
            if self.via_v6 is not None:
                # todo add logger
                # logger.warning("via_v6 has no effect for REDIRECT")
                print("via_v6 has no effect for REDIRECT")

        return self


class CustomRulesEndpoint(BaseEndpoint):
    """Endpoint for managing custom DNS rules."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.CUSTOM_RULES

    def list(self, profile_id: str, folder_id: Optional[int] = None) -> list[CustomRule]:
        """Return custom rules in a folder. For root folder, omit the folder ID.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            folder_id (Optional[int]): Folder ID (None for root). Defaults to None.

        Returns:
            list[listCustomRuleItem]: list of custom rule items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-rules-folder-id
        """
        url = self._url.format(profile_id=profile_id)
        url += f"/{'' if folder_id is None else folder_id}"

        return self._list(url=url, model=CustomRule, key="rules")

    def modify(
        self, profile_id: str, form_data: ModifyCustomRuleFormData
    ) -> list[ModifiedCustomRule]:
        """Modify an existing custom rule.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (CustomRuleFormData): Form data for rule modification.

        Returns:
            bool: list of modified items.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-rules
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(url, data=form_data.model_dump_json(), headers=headers)
        check_response(response)
        data = response.json()
        return create_list_of_items(ModifiedCustomRule, data["body"]["rules"])

    def create(
        self, profile_id: str, form_data: CreateCustomRuleFormData
    ) -> list[ModifiedCustomRule]:
        """Create one or more custom rules.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (CustomRuleFormData): Form data for rule creation.

        Returns:
            list[CreateCustomRuleItem]: list of created custom rule items.

        Reference:
            https://docs.controld.com/reference/post_profiles-profile-id-rules
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(url, data=form_data.model_dump_json(), headers=headers)
        check_response(response)

        data = response.json()
        return create_list_of_items(ModifiedCustomRule, data["body"]["rules"])

    def delete(self, profile_id: str, hostname: str) -> bool:
        """Delete one or more custom rules.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            hostname (str): Hostname to delete.

        Returns:
            bool: True if rules were deleted successfully.

        Reference:
            https://docs.controld.com/reference/delete_profiles-profile-id-rules-hostname
        """
        url = self._url.format(profile_id=profile_id)
        url = url + f"/{hostname}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.delete(url, headers=headers)
        check_response(response)
        return True
