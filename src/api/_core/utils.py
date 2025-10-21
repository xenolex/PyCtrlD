from __future__ import annotations

import ipaddress
import re
from typing import TYPE_CHECKING

from requests import Response, Session

if TYPE_CHECKING:
    from typing import Any, Iterable, Optional


class BaseEndpoint:
    def __init__(self, token: str) -> None:
        self._session = Session()

        self._session.headers.update(
            {"Authorization": f"Bearer {token}", "accept": "application/json"}
        )

        self._url = ""

    def __repr__(self):
        return f"<{self.__class__.__name__} url={self._url}>"

    def get_raw_response(self, url, params: Optional[dict] = None):
        if params is None:
            params = {}
        return self._session.get(url, params=params)

    def _request(self, method, url, params: Optional[dict] = None, data=None, headers=None):
        response = self._session.request(
            method=method, url=url, params=params, data=data, headers=headers
        )
        check_response(response)
        data = response.json()

        return data["body"]

    def _list(self, url, model, key, params: Optional[dict] = None):
        data = self._request("GET", url, params=params)
        return create_list_of_items(model, data[key])

    def _create(self, url, model, key, params: Optional[dict] = None):
        data = self._request("POST", url, params=params)
        return create_list_of_items(model, data[key])

    def _delete(self, url, data: Optional[str | dict] = None):
        self._request(
            "DELETE",
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )


def check_response(response: Response):
    class ApiError(Exception):
        def __init__(self, response: Response):
            data = response.json()["error"]

            message = (
                f"HTTP Status: {response.status_code} | "
                f"Error Code: {data['code']} | Message: {data['message']}"
            )

            super().__init__(message)

    if response.status_code != 200:
        raise ApiError(response)


def create_list_of_items(model: type, items: Iterable) -> list[Any]:
    """
    Validate an iterable of raw dict items into a list of model instances.

    The model is expected to expose a `model_validate` classmethod (e.g. Pydantic model).
    Strict validation is enforced to surface schema mismatches early.

    Args:
        model: The model class (e.g., a Pydantic BaseModel subclass) with model_validate.
        items: Iterable of raw item payloads (dict-like).

    Returns:
        list[Any]: list of validated model instances.
    """
    out_list: list[Any] = []

    for item in items:
        instance = model.model_validate(item, strict=True)  # type: ignore[attr-defined]
        out_list.append(instance)

    return out_list


def check_via_is_proxy_identifier(via: str | None):
    """Check that via field contains a valid 3-letter uppercase proxy identifier."""
    if not all((via is not None, str(via).isupper(), len(str(via)) == 3)):
        raise ValueError(f"via field must be a valid proxy identifier, got: {via}")


def check_via_is_record_or_cname(via: str | None):
    """Check that via field contains either a valid IPv4 address or domain name."""
    if via is None:
        raise ValueError("via field is required when do=SPOOF")

    is_ipv4 = True
    is_cname = True

    try:
        ipaddress.IPv4Address(via)
    except ipaddress.AddressValueError:
        is_ipv4 = False

    # Basic domain name validation regex
    domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(domain_pattern, via):
        is_cname = False

    if not is_ipv4 and not is_cname:
        raise ValueError(f"via field must be a valid IPv4 address or domain name, got: {via}")


def check_via_v6_is_aaaa_record(via_v6: str | None):
    """Check that via_v6 field contains a valid IPv6 address (AAAA record)."""
    if via_v6 is not None:
        try:
            ipaddress.IPv6Address(via_v6)
        except ipaddress.AddressValueError:
            raise ValueError(f"via_v6 field must be a valid IPv6 address, got: {via_v6}")
