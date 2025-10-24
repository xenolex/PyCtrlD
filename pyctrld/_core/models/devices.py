"""Device models for ControlD API.

This module provides data models for DNS devices/resolvers including device
configurations, settings, statistics levels, and device type categorizations.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import field_validator, model_validator

from pyctrld._core.models.common import ConfiguratedBaseModel, Status


class Stats(Enum):
    """Analytics/statistics level for device logging.

    Attributes:
        OFF: Analytics disabled (0).
        BASIC: Basic analytics level (1).
        FULL: Full analytics level (2).
    """

    OFF = 0
    BASIC = 1
    FULL = 2


class Ddns(ConfiguratedBaseModel):
    """Dynamic DNS configuration for a device.

    Attributes:
        status: Whether DDNS is enabled or disabled.
        subdomain: The DDNS subdomain.
        hostname: The full DDNS hostname.
        record: The DNS record value.
    """

    status: Status
    subdomain: str
    hostname: str
    record: str


class DdnsExt(ConfiguratedBaseModel):
    """Extended DDNS configuration for IP learning.

    Attributes:
        status: Whether extended DDNS is enabled or disabled.
        host: The DDNS hostname to query for IP learning.
    """

    status: Status
    host: str


class Resolvers(ConfiguratedBaseModel):
    """DNS resolver endpoints for a device.

    Attributes:
        uid: Unique identifier for the resolver.
        doh: DNS over HTTPS endpoint URL.
        dot: DNS over TLS endpoint URL.
        v4: IPv4 resolver address(es).
        v6: IPv6 resolver addresses.
    """

    uid: str
    doh: str
    dot: str
    v4: Optional[str | list[str]] = None
    v6: Optional[list[str]] = None


class LegacyIPv4(ConfiguratedBaseModel):
    """Legacy IPv4 DNS resolver configuration.

    Attributes:
        resolver: The legacy IPv4 resolver address.
        status: Whether the legacy resolver is enabled or disabled.
    """

    resolver: str
    status: Status


class Profile(ConfiguratedBaseModel):
    """DNS profile associated with a device.

    Attributes:
        PK: Primary key (unique identifier) of the profile.
        updated: Timestamp of last profile update.
        name: Profile name.
    """

    PK: str
    updated: int
    name: str


class CtrlD(ConfiguratedBaseModel):
    """ControlD daemon configuration status.

    Attributes:
        last_fetch: Timestamp of last configuration fetch.
        status: Whether the daemon is enabled or disabled.
        version: Version string of the daemon.
    """

    last_fetch: int
    status: Status
    version: str


class Device(ConfiguratedBaseModel):
    """Complete device/resolver configuration model.

    Represents a DNS device with all its configuration, resolvers, and settings.

    Attributes:
        PK: Primary key (unique identifier) of the device.
        ts: Timestamp of device creation.
        name: Device name.
        stats: Analytics level for the device.
        device_id: Unique device identifier.
        status: Device status (enabled/disabled).
        restricted: Whether device is restricted to authorized IPs only.
        learn_ip: Whether automatic IP learning is enabled.
        desc: Optional device description.
        ddns: Dynamic DNS configuration.
        ddns_ext: Extended DDNS configuration for IP learning.
        resolvers: DNS resolver endpoints for this device.
        legacy_ipv4: Legacy IPv4 resolver configuration.
        profile: The DNS profile enforced on this device.
        icon: Device icon/type identifier.
        bump_tls: Whether TLS bumping/ECH support is enabled.
        user: User identifier who owns the device.
        client_count: Number of clients using this device.
        ip_count: Number of learned IP addresses.
        last_activity: Timestamp of last device activity.
        clients: Dictionary of client information.
        ctrld: ControlD daemon configuration status.
    """

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
    """Device settings configuration.

    Attributes:
        stats: Analytics level setting.
        legacy_ipv4_status: Legacy IPv4 resolver status.
        learn_ip: IP learning status.
    """

    stats: Optional[Stats] = None
    legacy_ipv4_status: Optional[Status] = None
    learn_ip: Optional[Status] = None

    @field_validator("stats", mode="before")
    @classmethod
    def set_stats(cls, value):
        return Stats(value)


class Icon(ConfiguratedBaseModel):
    """Device icon/type definition.

    Attributes:
        name: Icon display name.
        settings: Default settings for this device type.
        highlight: Optional list of highlighted features.
        require: Optional list of required features.
    """

    name: str
    settings: Settings
    highlight: Optional[list[str]] = None
    require: Optional[list[str]] = None


class BaseIcons(ConfiguratedBaseModel):
    """Base class for icon collections with hyphen-to-underscore conversion.

    This model automatically converts hyphenated keys to underscored keys
    to match Python naming conventions.
    """

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
    """Operating system device icons.

    Attributes:
        mobile_ios: iOS mobile device icon.
        mobile_android: Android mobile device icon.
        desktop_windows: Windows desktop icon.
        desktop_mac: macOS desktop icon.
        desktop_linux: Linux desktop icon.
    """

    mobile_ios: Icon
    mobile_android: Icon
    desktop_windows: Icon
    desktop_mac: Icon
    desktop_linux: Icon


class Os(ConfiguratedBaseModel):
    """Operating system device type category.

    Attributes:
        name: Category name.
        icons: Collection of OS device icons.
    """

    name: str
    icons: OsIcons


class BrowserIcons(BaseIcons):
    """Browser device icons.

    Attributes:
        browser_chrome: Chrome browser icon.
        browser_firefox: Firefox browser icon.
        browser_edge: Edge browser icon.
        browser_brave: Brave browser icon.
        browser_other: Other browser icon.
    """

    browser_chrome: Icon
    browser_firefox: Icon
    browser_edge: Icon
    browser_brave: Icon
    browser_other: Icon


class Browser(ConfiguratedBaseModel):
    """Browser device type category.

    Attributes:
        name: Category name.
        icons: Collection of browser device icons.
    """

    name: str
    icons: BrowserIcons


class TvIcons(BaseIcons):
    """TV/streaming device icons.

    Attributes:
        tv: Generic TV icon.
        tv_apple: Apple TV icon.
        tv_android: Android TV icon.
        tv_firetv: Fire TV icon.
        tv_samsung: Samsung TV icon.
    """

    tv: Icon
    tv_apple: Icon
    tv_android: Icon
    tv_firetv: Icon
    tv_samsung: Icon


class Tv(ConfiguratedBaseModel):
    """TV device type category.

    Attributes:
        name: Category name.
        icons: Collection of TV device icons.
    """

    name: str
    icons: TvIcons


class RouterIcons(BaseIcons):
    """Router device icons.

    Attributes:
        router: Generic router icon.
        router_openwrt: OpenWrt router icon.
        router_ubiquiti: Ubiquiti router icon.
        router_asus: ASUS router icon.
        router_ddwrt: DD-WRT router icon.
        router_linux: Linux router icon.
        router_glinet: GL.iNet router icon.
        router_synology: Synology router icon.
        router_freshtomato: FreshTomato router icon.
        router_windows: Windows router icon.
        router_pfsense: pfSense router icon.
        router_opnsense: OPNsense router icon.
        router_firewalla: Firewalla router icon.
    """

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
    """Router device type category.

    Attributes:
        name: Category name.
        icons: Collection of router device icons.
        setup_url: URL to setup instructions.
    """

    name: str
    icons: RouterIcons
    setup_url: str


class DeviceTypes(ConfiguratedBaseModel):
    """Complete device types categorization.

    Contains all available device type categories and their icons.

    Attributes:
        os: Operating system devices category.
        browser: Browser devices category.
        tv: TV/streaming devices category.
        router: Router devices category.
    """

    os: Os
    browser: Browser
    tv: Tv
    router: Router
