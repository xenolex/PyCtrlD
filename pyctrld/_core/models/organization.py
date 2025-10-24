from __future__ import annotations

from pyctrld._core.models.common import ConfiguratedBaseModel, Count, Status


class Members(Count):
    pass


class Profiles(Count):
    max: int


class Users(Profiles):
    price: int


class Routers(Users):
    pass


class SubOrganizations(Profiles):
    pass


class BaseOrganization(ConfiguratedBaseModel):
    website: str
    address: str
    max_profiles: int
    status: Status
    stats_endpoint: str
    max_users: int
    max_legacy_resolvers: int
    name: str
    date: str
    max_routers: int
    contact_email: str
    PK: int
    members: Members
    profiles: Profiles
    users: Users
    routers: Routers
    sub_organizations: SubOrganizations


class Organization(BaseOrganization):
    price_users: int
    price_routers: int
    max_sub_orgs: int


class Permission(ConfiguratedBaseModel):
    level: int
    printable: bool


class Member(ConfiguratedBaseModel):
    PK: str
    email: str
    last_active: int
    twofa: int
    status: Status
    permission: Permission


class ParentOrg(ConfiguratedBaseModel):
    name: str
    PK: str


class ParentProfile(ConfiguratedBaseModel):
    name: str
    PK: str
    updated: int


class SubOrganization(BaseOrganization):
    contact_name: str
    parent_org: ParentOrg
    twofa_req: int
    parent_profile: ParentProfile
