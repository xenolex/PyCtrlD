from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator

from api.profiles._base import (
    BaseEndpoint,
    check_response,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
    create_list_of_items,
)
from api.profiles._models.custom_rules import (
    CustomRule,
    ModifiedCustomRule,
)
from api.profiles.constants import Do, Endpoints, Status


class __BaseCustomRuleFormData(BaseModel):
    via: Optional[str] = None
    via_v6: Optional[str] = None
    group: Optional[int] = None
    hostnames: List[str]


class CreateCustomRuleFormData(__BaseCustomRuleFormData):
    """Form data for creating custom rules.

    Args:
        do (Do): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Rule status. (ENABLED or DISABLED).
        via (Optional[str]): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                   If REDIRECT, this must be a valid proxy identifier.
        via_v6 (Optional[str]): If SPOOF this can be a valid IPv6 address (AAAA record).
        group (Optional[int]): Group ID to organize rules.
        hostnames (List[str]): List of hostnames this rule applies to. len(hostnames) rules will be created
    """

    do: Do
    status: Status

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)

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
        do (Optional[Do]): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Optional[Status]): Rule status. (ENABLED or DISABLED).
        via (str): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                   If REDIRECT, this must be a valid proxy identifier.
        via_v6 (Optional[str]): If SPOOF this can be a valid IPv6 address (AAAA record).
        group (int): Group ID to organize rules.
        hostnames (List[str]): List of hostnames this rule applies to. len(hostnames) rules will be created
    """

    do: Optional[Do] = None
    status: Optional[Status] = None

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return None if v is None else Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return None if v is None else Status(v)

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

    def list(self, profile_id: str, folder_id: Optional[int] = None) -> List[CustomRule]:
        """Return custom rules in a folder. For root folder, omit the folder ID.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            folder_id (Optional[int]): Folder ID (None for root). Defaults to None.

        Returns:
            List[ListCustomRuleItem]: List of custom rule items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-rules-folder-id
        """
        url = self._url.format(profile_id=profile_id)
        url += f"/{'' if folder_id is None else folder_id}"

        response = self._session.get(url)
        check_response(response)

        data = response.json()
        return create_list_of_items(CustomRule, data["body"]["rules"])

    def modify(
        self, profile_id: str, form_data: ModifyCustomRuleFormData
    ) -> List[ModifiedCustomRule]:
        """Modify an existing custom rule.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (CustomRuleFormData): Form data for rule modification.

        Returns:
            bool: List of modified items.

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
    ) -> List[ModifiedCustomRule]:
        """Create one or more custom rules.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (CustomRuleFormData): Form data for rule creation.

        Returns:
            List[CreateCustomRuleItem]: List of created custom rule items.

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
