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
    def __init__(self, token: str):
        self.token = token

    @cached_property
    def custom_rules(self):
        return CustomRulesEndpoint(self.token)

    @cached_property
    def default_rule(self):
        return DefaultRuleEndpoint(self.token)

    @cached_property
    def filters(self):
        return FiltersEndpoint(self.token)

    @cached_property
    def list_proxies(self):
        return ListProxiesEndpoint(self.token)

    @cached_property
    def profiles(self):
        return ProfilesEndpoint(self.token)

    @cached_property
    def rule_folders(self):
        return RuleFoldersEndpoint(self.token)

    @cached_property
    def services(self):
        return ServicesEndpoint(self.token)
