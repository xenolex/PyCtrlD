from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import field_validator, model_validator

from pyctrld._core.models.common import ConfiguratedBaseModel, Status


class Stats(Enum):
    OFF = 0
    BASIC = 1
    FULL = 2


class Ddns(ConfiguratedBaseModel):
    status: Status
    subdomain: str
    hostname: str
    record: str


class DdnsExt(ConfiguratedBaseModel):
    status: Status
    host: str


class Resolvers(ConfiguratedBaseModel):
    uid: str
    doh: str
    dot: str
    v4: Optional[str | list[str]] = None
    v6: Optional[list[str]] = None


class LegacyIPv4(ConfiguratedBaseModel):
    resolver: str
    status: Status


class Profile(ConfiguratedBaseModel):
    PK: str
    updated: int
    name: str


class CtrlD(ConfiguratedBaseModel):
    last_fetch: int
    status: Status
    version: str


class Device(ConfiguratedBaseModel):
    PK: str
    ts: int
    name: str
    stats: Optional[Stats] = None
    device_id: str
    status: Status
    restricted: Optional[Status] = None
    learn_ip: Status
    desc: Optional[str] = None
    ddns: Optional[Ddns] = None
    ddns_ext: Optional[DdnsExt] = None
    resolvers: Resolvers
    legacy_ipv4: Optional[LegacyIPv4] = None
    profile: Profile
    icon: Optional[str] = None
    bump_tls: Optional[Status] = None
    user: str
    client_count: int
    ip_count: Optional[int] = None
    last_activity: Optional[int] = None
    clients: Optional[dict[str, Any]] = None
    ctrld: Optional[CtrlD] = None

    @field_validator("resolvers", mode="before")
    @classmethod
    def set_resolvers(cls, value):
        return Resolvers.model_validate(value, strict=True)

    @field_validator("stats", mode="before")
    @classmethod
    def set_stats(cls, value):
        return Stats(value)


class Settings(ConfiguratedBaseModel):
    stats: Optional[Stats] = None
    legacy_ipv4_status: Optional[Status] = None
    learn_ip: Optional[Status] = None

    @field_validator("stats", mode="before")
    @classmethod
    def set_stats(cls, value):
        return Stats(value)


class Icon(ConfiguratedBaseModel):
    name: str
    settings: Settings
    highlight: Optional[list[str]] = None
    require: Optional[list[str]] = None


class BaseIcons(ConfiguratedBaseModel):
    @model_validator(mode="before")
    @classmethod
    def validate_values(cls, values):
        for key in values.copy():
            if "-" in key:
                new_key = key.replace("-", "_")
                values[new_key] = values[key]
                del values[key]
        return values


class OsIcons(BaseIcons):
    mobile_ios: Icon
    mobile_android: Icon
    desktop_windows: Icon
    desktop_mac: Icon
    desktop_linux: Icon


class Os(ConfiguratedBaseModel):
    name: str
    icons: OsIcons


class BrowserIcons(BaseIcons):
    browser_chrome: Icon
    browser_firefox: Icon
    browser_edge: Icon
    browser_brave: Icon
    browser_other: Icon


class Browser(ConfiguratedBaseModel):
    name: str
    icons: BrowserIcons


class TvIcons(BaseIcons):
    tv: Icon
    tv_apple: Icon
    tv_android: Icon
    tv_firetv: Icon
    tv_samsung: Icon


class Tv(ConfiguratedBaseModel):
    name: str
    icons: TvIcons


class RouterIcons(BaseIcons):
    router: Icon
    router_openwrt: Icon
    router_ubiquiti: Icon
    router_asus: Icon
    router_ddwrt: Icon
    router_linux: Icon
    router_glinet: Icon
    router_synology: Icon
    router_freshtomato: Icon
    router_windows: Icon
    router_pfsense: Icon
    router_opnsense: Icon
    router_firewalla: Icon


class Router(ConfiguratedBaseModel):
    name: str
    icons: RouterIcons
    setup_url: str


class DeviceTypes(ConfiguratedBaseModel):
    os: Os
    browser: Browser
    tv: Tv
    router: Router
