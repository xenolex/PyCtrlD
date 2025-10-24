from __future__ import annotations

from pyctrld._api import ControlDApi
from pyctrld.api.access import AccessEndpoint, AccessFormData
from pyctrld.api.account import AccountEndpoint
from pyctrld.api.analytics import AnalyticsEndpoint
from pyctrld.api.billing import BillingEndpoint
from pyctrld.api.devices import (
    CreateDeviceFormData,
    DevicesEndpoint,
    DeviceStatus,
    ModifyDeviceFormData,
)
from pyctrld.api.misc import MiscEndpoint
from pyctrld.api.mobile_config import MobileConfigEndpoint
from pyctrld.api.organization import (
    CreateSubOrganizationFromData,
    ModifyOrganizationFromData,
    OrganizationEndpoint,
)
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
)
from pyctrld.api.profiles.services import (
    ServicesEndpoint as ProfileServicesEndpoint,
)
from pyctrld.api.services import ServicesEndpoint

__all__ = [
    # Common
    "ControlDApi",
    # ProfilesAPI
    "ProfilesAPI",
    # Endpoint classes
    "AccessEndpoint",
    "AccountEndpoint",
    "AnalyticsEndpoint",
    "BillingEndpoint",
    "DevicesEndpoint",
    "MiscEndpoint",
    "MobileConfigEndpoint",
    "OrganizationEndpoint",
    "CustomRulesEndpoint",
    "DefaultRuleEndpoint",
    "FiltersEndpoint",
    "ListProxiesEndpoint",
    "ProfilesEndpoint",
    "RuleFoldersEndpoint",
    "ServicesEndpoint",
    "ProfileServicesEndpoint",
    # Form data classes
    "AccessFormData",
    "CreateDeviceFormData",
    "ModifyDeviceFormData",
    "CreateSubOrganizationFromData",
    "ModifyOrganizationFromData",
    # Enums and types
    "DeviceStatus",
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
