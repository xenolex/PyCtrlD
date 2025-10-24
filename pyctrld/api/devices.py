from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from pyctrld._core.models.common import BaseFormData
from pyctrld._core.models.devices import (
    Device,
    DeviceTypes,
    Stats,
)
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint

_icon_list = Literal[
    "mobile-ios",
    "mobile-android",
    "phone",
    "desktop-windows",
    "desktop-mac",
    "desktop-linux",
    "browser-chrome",
    "browser-firefox",
    "browser-edge",
    "browser-brave",
    "browser-other",
    "tv",
    "tv-apple",
    "tv-android",
    "tv-firetv",
    "tv-samsung",
    "router",
    "router-openwrt",
    "router-ubiquiti",
    "router-asus",
    "router-ddwrt",
]


class CreateDeviceFormData(BaseFormData):
    """
    Create a new Device.

    Args:
        name: Device name (required)
        profile_id: Primary key of main profile to enforce on this device (optional)
        profile_id2: Primary key of a second profile to enforce (optional)
        icon: Device icon/type (required)
        stats: Set analytics level on device. OFF, BASIC, FULL (optional)
        legacy_ipv4_status: Set this to 1 to generate a legacy IPv4 (and IPv6) DNS resolver. (optional)
        learn_ip: Enable or disable automatic IP learning and logging. 0 to disable, 1 to enable. (optional)
        restricted: Make this device restricted, only previously authorized IPs will be able to query against it (optional)
        desc: Add a description or comment to the device (optional)
        ddns_status: Status of DDNS endpoint that exposes last used IP. (optional)
        ddns_subdomain:DDNS subdomain to expose the IP on (optional)
        ddns_ext_status: Status of DDNS based IP learning (optional)
        ddns_ext_host: DDNS hostname to query to learn new IPs (optional)
        remap_device_id: Remap source device + client ID to a new device (optional)
        remap_client_id: Remap source device + client ID to a new device (optional)
    """

    name: str
    profile_id: str
    profile_id2: Optional[str] = None
    icon: _icon_list
    stats: Optional[Stats | Literal["OFF", "BASIC", "FULL"]] = None
    legacy_ipv4_status: Optional[bool] = None
    learn_ip: Optional[bool] = None
    restricted: Optional[bool] = None
    desc: Optional[str] = None
    ddns_status: Optional[bool] = None
    ddns_subdomain: Optional[str] = None
    ddns_ext_status: Optional[int] = None
    ddns_ext_host: Optional[bool] = None
    remap_device_id: Optional[str] = None
    remap_client_id: Optional[str] = None


class DeviceStatus(Enum):
    PENDING = 0
    ACTIVE = 1
    SOFT_DISABLED = 2
    HARD_DISABLED = 3


class ModifyDeviceFormData(BaseFormData):
    """
    Create a new Device.

    Args:
        name: New Device name
        profile_id: Primary key of main profile to enforce on this device
        profile_id2: Primary key of a second profile to enforce -1 to remove.
        icon: Device icon/type (required)
        stats: Set analytics level on device. OFF, BASIC, FUL
        legacy_ipv4_status: Set this to 1 to generate a legacy IPv4 (and IPv6) DNS resolver, 0 to remove existing one.
        learn_ip: Make this device restricted. 0 to disable, 1 to enable.
        restricted: Make this device restricted, only previously authorized IPs will be able to query against it
        bump_tls: Enable or disable experimental ECH support and TLS bumping
        desc: Add a description or comment to the device
        ddns_status: Status of public DDNS endpoint. 1 = enabled, 0 = disable.
        ddns_subdomain: DDNS subdomain to expose the IP on
        status: Update device status. 0 - pending, 1 - active, 2 - soft disabled, 3 - hard disabled
        ctrld_custom_config: ctrld .toml config file to deploy

    """

    name: Optional[str] = None
    profile_id: Optional[str] = None
    profile_id2: Optional[str] = None
    stats: Optional[Stats | Literal["OFF", "BASIC", "FULL"]] = None
    legacy_ipv4_status: Optional[bool] = None
    learn_ip: Optional[bool] = None
    restricted: Optional[bool] = None
    desc: Optional[str] = None
    ddns_status: Optional[bool] = None
    ddns_subdomain: Optional[str] = None
    ddns_ext_status: Optional[bool] = None
    ddns_ext_host: Optional[str] = None
    status: Optional[DeviceStatus] = None
    ctrld_custom_config: Optional[str] = None


class DevicesEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)

        self._url = Endpoints.DEVICES

    def list_all_devices(self, filter: Literal["all", "users", "routers"] = "all") -> list[Device]:
        """
        list all devices that are associated with an account.

        Args:
            filter: Filter devices by type.

        Returns:
            list[Device]: list all devices that are associated with an account.

        Reference:
            https://docs.controld.com/reference/get_devices
        """
        match filter:
            case "users":
                url = self._url + "/users"
            case "routers":
                url = self._url + "/routers"
            case _:
                url = self._url

        return self._list(url=url, model=Device, key="devices")

    def create_device(self, form_data: CreateDeviceFormData) -> Device:
        """
        Create a new Device. This endpoint will return DNS resolvers specific to this Device.

        Args:
            form_data: Creation form data.

        Returns:
            Device: Device object

        Reference:
            https://docs.controld.com/reference/post_devices
        """

        data = self._request(
            method="POST",
            url=self._url,
            data=form_data.model_dump_json(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return Device.model_validate(data, strict=True)

    def list_device_types(self) -> DeviceTypes:
        """
        Return a list of allowed device types.

        Returns:
            DeviceTypes: Return a list of allowed device types.

        Reference:
            https://docs.controld.com/reference/get_devices-types
        """
        data = self._request(
            method="GET",
            url=self._url + "/types",
        )
        return DeviceTypes.model_validate(data["types"], strict=True)

    def modify_device(self, device_id: str, form_data: ModifyDeviceFormData) -> Device:
        """
        Modify an existing Device and its settings.

        Args:
            device_id: Primary key (PK) of the device.
            form_data: Fields to update.

        Returns:
            list[Device]: Updated device.
        """

        data = self._request(
            method="PUT",
            url=self._url + f"/{device_id}",
            data=form_data.model_dump_json(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return Device.model_validate(data, strict=True)

    def delete_device(self, device_id: str) -> bool:
        """
        Delete a Device. This will break DNS on any physical gadget that uses this Device's unique DNS resolvers.

        Returns:
            DeleteDevicesResult: True if the device was deleted successfully.
        """

        self._delete(self._url + f"/{device_id}")
        return True
