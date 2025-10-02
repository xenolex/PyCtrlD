from dataclasses import asdict, dataclass
from typing import List, Optional

from api.profiles._base import (
    BaseEndpoint,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
)
from api.profiles._models.custom_rules import CreateCustomRuleItem, ListCustomRuleItem
from api.profiles.constants import Do, Status


@dataclass
class CustomRuleFormData:
    """Form data for creating and modifying custom rules.

    Args:
        do (Do): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Rule status. (ENABLED or DISABLED).
        via (str): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                   If REDIRECT, this must be a valid proxy identifier.
        via_v6 (Optional[str]): If SPOOF this can be a valid IPv6 address (AAAA record).
        group (int): Group ID to organize rules.
        hostnames (List[str]): List of hostnames this rule applies to.
    """

    do: Do
    status: Status
    via: str
    via_v6: Optional[str]
    group: int
    hostnames: List[str]

    def __init__(
        self,
        do: Do,
        status: Status,
        via: str,
        via_v6: Optional[str],
        group: int,
        hostnames: List[str],
    ) -> None:
        self.do = Do(do)
        self.status = Status(status)
        self.via = via
        self.via_v6 = via_v6
        self.group = group
        self.hostnames = hostnames

        if do == Do.SPOOF:
            check_via_is_record_or_cname(self.via)
            check_via_v6_is_aaaa_record(self.via_v6)

        if do == Do.REDIRECT:
            check_via_is_proxy_identifier(self.via)
            if via_v6 is not None:
                # todo add logger
                # logger.warning("via_v6 has no effect for REDIRECT")
                print("via_v6 has no effect for REDIRECT")


class CustomRulesEndpoint(BaseEndpoint):
    """Endpoint for managing custom DNS rules."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = self._url + "/{profile_id}/rules"

    def list(self, profile_id: str, folder_id: str) -> List[ListCustomRuleItem]:
        """Return custom rules in a folder. For root folder, omit the folder ID.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            folder_id (str): Folder ID (0 or omit for root).

        Returns:
            List[ListCustomRuleItem]: List of custom rule items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-rules-folder-id
        """
        url = self._url.format(profile_id=profile_id)
        url += f"/{folder_id}"
        response = self._session.get(url)
        response.raise_for_status()

        data = response.json()
        return [
            ListCustomRuleItem(
                PK=item["PK"],
                order=item["order"],
                group=item["group"],
                action=item["action"],
            )
            for item in data["body"]["rules"]
        ]

    def modify(self, profile_id: str, form_data: CustomRuleFormData) -> bool:
        """Modify an existing custom rule.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (CustomRuleFormData): Form data for rule modification.

        Returns:
            bool: True if rule was modified successfully.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-rules
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.put(url, data=asdict(form_data), headers=headers)
        response.raise_for_status()
        return True

    def create(self, profile_id: str, form_data: CustomRuleFormData) -> List[CreateCustomRuleItem]:
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

        response = self._session.post(url, data=asdict(form_data), headers=headers)
        response.raise_for_status()

        data = response.json()
        return [
            CreateCustomRuleItem(
                do=item.get("do"),
                status=item.get("status"),
                via=item.get("via"),
                order=item.get("order"),
                group=item.get("group"),
            )
            for item in data["body"]["rules"]
        ]

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
        response.raise_for_status()
        return True
