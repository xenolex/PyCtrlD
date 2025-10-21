from __future__ import annotations

import sys

sys.path.extend(["./", "./src/"])

import os
from pprint import pprint
from random import randint

import pytest
from dotenv import load_dotenv

from api._core.models.devices import (
    Browser,
    BrowserIcons,
    CtrlD,
    Ddns,
    DdnsExt,
    Device,
    DeviceTypes,
    Icon,
    LegacyIPv4,
    Os,
    OsIcons,
    Profile,
    Resolvers,
    Router,
    RouterIcons,
    Settings,
    Tv,
    TvIcons,
)
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.devices import CreateDeviceFormData, DevicesEndpoint, ModifyDeviceFormData
from tests.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")
test_device_id2 = os.getenv("TEST_DEVICE_ID2", "")


class TestDevices:
    api = DevicesEndpoint(token)
    default_name = "Default-Device-Name"

    def test_list_all_devices(self):
        check_api_list_endpoint(self.api, model=Device, method_name="list_all_devices")
        check_api_list_endpoint(
            self.api, model=Device, method_name="list_all_devices", api_kwargs={"filter": "users"}
        )
        check_api_list_endpoint(
            self.api, model=Device, method_name="list_all_devices", api_kwargs={"filter": "routers"}
        )

    @pytest.mark.skip(reason="too many notifications")
    def test_create_device(self):
        name = f"test{randint(0, 99999)}"
        form_data = CreateDeviceFormData(
            name=name, profile_id=profile_id, icon="browser-other", learn_ip=True
        )
        created_device = self.api.create_device(form_data)

        assert name == created_device.name

    def test_modify_device(self):
        name = f"test{randint(0, 99999)}"
        form_data = ModifyDeviceFormData(name=name)
        updated_device = self.api.modify_device(test_device_id2, form_data)
        assert name == updated_device.name

        form_data = ModifyDeviceFormData(name=self.default_name)
        updated_device = self.api.modify_device(test_device_id2, form_data)

        assert self.default_name == updated_device.name

    def test_delete_device(self):
        lst = self.api.list_all_devices()
        for device in lst:
            if device.name.startswith("test"):
                assert self.api.delete_device(device.device_id)

    def test_list_device_types(self):
        devicetypes = self.api.list_device_types()
        for key in devicetypes.model_fields_set:
            check_key_in_model(key, DeviceTypes)
            match key:
                case "os":
                    for os_key in devicetypes.os.model_fields_set:
                        check_key_in_model(os_key, Os)
                        if os_key == "icons":
                            for icon_key in devicetypes.os.icons.model_fields_set:
                                check_key_in_model(icon_key, OsIcons)
                                dump = devicetypes.os.icons.model_dump()
                                for dump_key in dump[icon_key]:
                                    check_key_in_model(dump_key, Icon)
                                    sub_dump = dump[icon_key][dump_key]
                                    if dump_key == "settings":
                                        for sub_dump_key in sub_dump:
                                            check_key_in_model(sub_dump_key, Settings)
                case "tv":
                    for tv_key in devicetypes.tv.model_fields_set:
                        check_key_in_model(tv_key, Tv)
                        if tv_key == "icons":
                            for icon_key in devicetypes.tv.icons.model_fields_set:
                                check_key_in_model(icon_key, TvIcons)
                                dump = devicetypes.tv.icons.model_dump()
                                for dump_key in dump[icon_key]:
                                    check_key_in_model(dump_key, Icon)
                                    sub_dump = dump[icon_key][dump_key]
                                    if dump_key == "settings":
                                        for sub_dump_key in sub_dump:
                                            check_key_in_model(sub_dump_key, Settings)
                case "browser":
                    for browser_key in devicetypes.browser.model_fields_set:
                        check_key_in_model(browser_key, Browser)
                        if browser_key == "icons":
                            for icon_key in devicetypes.browser.icons.model_fields_set:
                                check_key_in_model(icon_key, BrowserIcons)
                                dump = devicetypes.browser.icons.model_dump()
                                for dump_key in dump[icon_key]:
                                    check_key_in_model(dump_key, Icon)
                                    sub_dump = dump[icon_key][dump_key]
                                    if dump_key == "settings":
                                        for sub_dump_key in sub_dump:
                                            check_key_in_model(sub_dump_key, Settings)
                case "router":
                    for router_key in devicetypes.router.model_fields_set:
                        check_key_in_model(router_key, Router)
                        if router_key == "icons":
                            for icon_key in devicetypes.router.icons.model_fields_set:
                                check_key_in_model(icon_key, RouterIcons)
                                dump = devicetypes.router.icons.model_dump()
                                for dump_key in dump[icon_key]:
                                    check_key_in_model(dump_key, Icon)
                                    sub_dump = dump[icon_key][dump_key]
                                    if dump_key == "settings":
                                        for sub_dump_key in sub_dump:
                                            check_key_in_model(sub_dump_key, Settings)
                case _:
                    assert False, f"Unknown device type: {key}"


def test_list_all_devices_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.DEVICES)

    data = response.json()
    items = data["body"]["devices"]
    for device in items:
        pprint(device)
        for key in device:
            check_key_in_model(key, Device)
            if key == "ctrd":
                for ctrld_key in device[key]:
                    check_key_in_model(ctrld_key, CtrlD)
            if key == "ddns" and device[key] is not None:
                for ddns_key in device[key]:
                    check_key_in_model(ddns_key, Ddns)
            if key == "ddns_ext" and device[key] is not None:
                for ddns_ext_key in device[key]:
                    check_key_in_model(ddns_ext_key, DdnsExt)
            if key == "resolvers" and device[key] is not None:
                for resolvers_key in device[key]:
                    check_key_in_model(resolvers_key, Resolvers)
            if key == "profile" and device[key] is not None:
                for profile_key in device[key]:
                    check_key_in_model(profile_key, Profile)
            if key == "legacy_ipv4" and device[key] is not None:
                for legacy_ipv4_key in device[key]:
                    check_key_in_model(legacy_ipv4_key, LegacyIPv4)
