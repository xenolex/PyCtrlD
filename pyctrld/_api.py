"""Main ControlD API client.

This module provides the primary interface for interacting with the ControlD API.
The ControlDApi class provides access to all API endpoints through cached properties.
"""

from __future__ import annotations

from functools import cached_property

from pyctrld.api.access import AccessEndpoint
from pyctrld.api.account import AccountEndpoint
from pyctrld.api.analytics import AnalyticsEndpoint
from pyctrld.api.billing import BillingEndpoint
from pyctrld.api.devices import DevicesEndpoint
from pyctrld.api.misc import MiscEndpoint
from pyctrld.api.mobile_config import MobileConfigEndpoint
from pyctrld.api.organization import OrganizationEndpoint
from pyctrld.api.profiles._api import ProfilesAPI
from pyctrld.api.services import ServicesEndpoint


class ControlDApi:
    """Main API client for interacting with ControlD services.

    This class provides a unified interface to all ControlD API endpoints.
    Each endpoint is exposed as a cached property, instantiated only when first accessed.

    Args:
        token: The API authentication bearer token.

    Attributes:
        access: Access endpoint for managing known IPs.
        account: Account endpoint for user data.
        analytics: Analytics endpoint for usage statistics.
        billing: Billing endpoint for subscription information.
        devices: Devices endpoint for managing DNS resolvers.
        misc: Miscellaneous endpoint for utility functions.
        mobile_config: Mobile config endpoint for device configurations.
        organization: Organization endpoint for managing organizations.
        profiles: Profiles API for managing DNS profiles and rules.
        services: Services endpoint for listing service categories.

    Example:
        >>> api = ControlDApi(token="your_api_token")
        >>> devices = api.devices.list_all_devices()
        >>> profiles = api.profiles.profiles.list()
    """

    def __init__(self, token: str) -> None:
        """Initialize the ControlD API client.

        Args:
            token: The API bearer token for authentication.
        """
        self._token = token

    @cached_property
    def access(self) -> AccessEndpoint:
        """Access endpoint for managing device IP access control.

        Returns:
            AccessEndpoint instance for IP management operations.
        """
        return AccessEndpoint(token=self._token)

    @cached_property
    def account(self) -> AccountEndpoint:
        """Account endpoint for retrieving user data.

        Returns:
            AccountEndpoint instance for account operations.
        """
        return AccountEndpoint(token=self._token)

    @cached_property
    def analytics(self) -> AnalyticsEndpoint:
        """Analytics endpoint for query statistics and metrics.

        Returns:
            AnalyticsEndpoint instance for analytics operations.
        """
        return AnalyticsEndpoint(token=self._token)

    @cached_property
    def billing(self) -> BillingEndpoint:
        """Billing endpoint for subscription and payment information.

        Returns:
            BillingEndpoint instance for billing operations.
        """
        return BillingEndpoint(token=self._token)

    @cached_property
    def devices(self) -> DevicesEndpoint:
        """Devices endpoint for managing DNS resolvers.

        Returns:
            DevicesEndpoint instance for device operations.
        """
        return DevicesEndpoint(token=self._token)

    @cached_property
    def misc(self) -> MiscEndpoint:
        """Miscellaneous endpoint for utility functions.

        Returns:
            MiscEndpoint instance for misc operations.
        """
        return MiscEndpoint(token=self._token)

    @cached_property
    def mobile_config(self) -> MobileConfigEndpoint:
        """Mobile config endpoint for device configuration profiles.

        Returns:
            MobileConfigEndpoint instance for mobile config operations.
        """
        return MobileConfigEndpoint(token=self._token)

    @cached_property
    def organization(self) -> OrganizationEndpoint:
        """Organization endpoint for managing organizations and sub-organizations.

        Returns:
            OrganizationEndpoint instance for organization operations.
        """
        return OrganizationEndpoint(token=self._token)

    @cached_property
    def profiles(self) -> ProfilesAPI:
        """Profiles API for managing DNS profiles, rules, and filters.

        Returns:
            ProfilesAPI instance for profile operations.
        """
        return ProfilesAPI(token=self._token)

    @cached_property
    def services(self) -> ServicesEndpoint:
        """Services endpoint for listing service categories.

        Returns:
            ServicesEndpoint instance for service operations.
        """
        return ServicesEndpoint(token=self._token)
