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
    def __init__(self, token: str):
        self._token = token

    @cached_property
    def access(self):
        return AccessEndpoint(token=self._token)

    @cached_property
    def accounts(self):
        return AccountEndpoint(token=self._token)

    @cached_property
    def analytics(self):
        return AnalyticsEndpoint(token=self._token)

    @cached_property
    def billing(self):
        return BillingEndpoint(token=self._token)

    @cached_property
    def devices(self):
        return DevicesEndpoint(token=self._token)

    @cached_property
    def misc(self):
        return MiscEndpoint(token=self._token)

    @cached_property
    def mobile_config(self):
        return MobileConfigEndpoint(token=self._token)

    @cached_property
    def organization(self):
        return OrganizationEndpoint(token=self._token)

    @cached_property
    def profiles(self):
        return ProfilesAPI(token=self._token)

    @cached_property
    def services(self):
        return ServicesEndpoint(token=self._token)
