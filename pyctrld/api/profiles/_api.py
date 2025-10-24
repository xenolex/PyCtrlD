"""Profiles API for ControlD.

This module provides a unified interface to all profile-related endpoints including
custom rules, default rules, filters, proxies, and services.
"""

from __future__ import annotations

from functools import cached_property

from pyctrld.api.profiles.custom_rules import CustomRulesEndpoint
from pyctrld.api.profiles.default_rule import DefaultRuleEndpoint
from pyctrld.api.profiles.filters import FiltersEndpoint
from pyctrld.api.profiles.list_proxies import ListProxiesEndpoint
from pyctrld.api.profiles.profiles import ProfilesEndpoint
from pyctrld.api.profiles.rule_folders import RuleFoldersEndpoint
from pyctrld.api.profiles.services import ServicesEndpoint


class ProfilesAPI:
    """Unified API for managing DNS profiles and related configurations.

    This class provides access to all profile-related endpoints through
    cached properties. Each endpoint is instantiated only when first accessed.

    Args:
        token: The API authentication bearer token.

    Attributes:
        custom_rules: Endpoint for managing custom DNS rules.
        default_rule: Endpoint for managing the default rule.
        filters: Endpoint for managing DNS filters.
        list_proxies: Endpoint for listing available proxies.
        profiles: Endpoint for managing DNS profiles.
        rule_folders: Endpoint for managing rule folders/groups.
        services: Endpoint for managing profile services.

    Example:
        >>> profiles_api = ProfilesAPI(token="your_token")
        >>> all_profiles = profiles_api.profiles.list()
        >>> custom_rules = profiles_api.custom_rules.list(profile_id="PK123")
    """

    def __init__(self, token: str) -> None:
        """Initialize the Profiles API.

        Args:
            token: Bearer token for API authentication.
        """
        self.token = token

    @cached_property
    def custom_rules(self) -> CustomRulesEndpoint:
        """Custom rules endpoint for managing DNS filtering rules.

        Returns:
            CustomRulesEndpoint instance for custom rule operations.
        """
        return CustomRulesEndpoint(self.token)

    @cached_property
    def default_rule(self) -> DefaultRuleEndpoint:
        """Default rule endpoint for managing the fallback DNS rule.

        Returns:
            DefaultRuleEndpoint instance for default rule operations.
        """
        return DefaultRuleEndpoint(self.token)

    @cached_property
    def filters(self) -> FiltersEndpoint:
        """Filters endpoint for managing DNS content filters.

        Returns:
            FiltersEndpoint instance for filter operations.
        """
        return FiltersEndpoint(self.token)

    @cached_property
    def list_proxies(self) -> ListProxiesEndpoint:
        """List proxies endpoint for retrieving available proxy servers.

        Returns:
            ListProxiesEndpoint instance for proxy listing operations.
        """
        return ListProxiesEndpoint(self.token)

    @cached_property
    def profiles(self) -> ProfilesEndpoint:
        """Profiles endpoint for managing DNS profiles.

        Returns:
            ProfilesEndpoint instance for profile operations.
        """
        return ProfilesEndpoint(self.token)

    @cached_property
    def rule_folders(self) -> RuleFoldersEndpoint:
        """Rule folders endpoint for organizing custom rules into groups.

        Returns:
            RuleFoldersEndpoint instance for rule folder operations.
        """
        return RuleFoldersEndpoint(self.token)

    @cached_property
    def services(self) -> ServicesEndpoint:
        """Services endpoint for managing service-based filtering in profiles.

        Returns:
            ServicesEndpoint instance for profile service operations.
        """
        return ServicesEndpoint(self.token)
