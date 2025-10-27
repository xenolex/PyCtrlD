"""Profiles API subpackage for ControlD.

This package contains all profile-related endpoints and form data classes for managing
DNS profiles, custom rules, filters, services, and rule folders in the ControlD API.
"""

from __future__ import annotations

from pyctrld.api.profiles._api import ProfilesAPI
from pyctrld.api.profiles.custom_rules import (
    CreateCustomRuleFormData,
    CustomRulesEndpoint,
    ModifyCustomRuleFormData,
)
from pyctrld.api.profiles.default_rule import (
    DefaultRuleEndpoint,
    DefaultRuleFormData,
)
from pyctrld.api.profiles.filters import (
    FiltersEndpoint,
    ModifyFilterFormData,
)
from pyctrld.api.profiles.list_proxies import ListProxiesEndpoint
from pyctrld.api.profiles.profiles import (
    CreateProfileFormData,
    ModifyOptionFormData,
    ModifyProfileFormData,
    ProfilesEndpoint,
)
from pyctrld.api.profiles.rule_folders import (
    CreateRuleFoldersFormData,
    RuleFoldersEndpoint,
    RuleFoldersFormData,
)
from pyctrld.api.profiles.services import (
    ModifyServiceFormData,
    ServicesEndpoint,
)

__all__ = [
    # Common
    "ProfilesAPI",
    # Endpoints
    "CustomRulesEndpoint",
    "DefaultRuleEndpoint",
    "FiltersEndpoint",
    "ListProxiesEndpoint",
    "ProfilesEndpoint",
    "RuleFoldersEndpoint",
    "ServicesEndpoint",
    # FormData - Custom Rules
    "CreateCustomRuleFormData",
    "ModifyCustomRuleFormData",
    # FormData - Default Rule
    "DefaultRuleFormData",
    # FormData - Filters
    "ModifyFilterFormData",
    # FormData - Profiles
    "CreateProfileFormData",
    "ModifyProfileFormData",
    "ModifyOptionFormData",
    # FormData - Rule Folders
    "CreateRuleFoldersFormData",
    "RuleFoldersFormData",
    # FormData - Services
    "ModifyServiceFormData",
]
