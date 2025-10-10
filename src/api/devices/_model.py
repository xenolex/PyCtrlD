from __future__ import annotations

from typing import Optional

from api._base import ConfiguratedBaseModel
from api.profiles.constants import Status


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
    v4: Optional[str] = None
    v6: Optional[str] = None


class LegacyIPv4(ConfiguratedBaseModel):
    resolver: str
    status: Status


class Profile(ConfiguratedBaseModel):
    PK: str
    updated: int
    name: str


class Device(ConfiguratedBaseModel):
    PK: str
    ts: int
    name: str
    stats: Optional[int] = None
    device_id: str
    status: Status
    restricted: Optional[int] = None
    learn_ip: int
    desc: Optional[str] = None
    ddns: Optional[Ddns] = None
    ddns_ext: Optional[DdnsExt] = None
    resolvers: Resolvers
    legacy_ipv4: Optional[LegacyIPv4] = None
    profile: Profile
    icon: Optional[str]
    bump_tls: Optional[int] = None


class OsIcons(ConfiguratedBaseModel):
    mobile_ios: str
    mobile_android: str
    desktop_windows: str
    desktop_mac: str
    desktop_linux: str


class Os(ConfiguratedBaseModel):
    name: str
    icons: OsIcons


class BrowserIcons(ConfiguratedBaseModel):
    browser_chrome: str
    browser_firefox: str
    browser_edge: str
    browser_brave: str
    browser_other: str


class Browser(ConfiguratedBaseModel):
    name: str
    icons: BrowserIcons


class TvIcons(ConfiguratedBaseModel):
    tv: str
    tv_apple: str
    tv_android: str
    tv_firetv: str
    tv_samsung: str


class Tv(ConfiguratedBaseModel):
    name: str
    icons: TvIcons


class RouterIcons(ConfiguratedBaseModel):
    router: str
    router_openwrt: str
    router_ubiquiti: str
    router_asus: str
    router_ddwrt: str


class Router(ConfiguratedBaseModel):
    name: str
    icons: TvIcons
    setup_url: str


class DeviceType(ConfiguratedBaseModel):
    os: Os
    browser: Browser
    tv: Tv
    router: Router
