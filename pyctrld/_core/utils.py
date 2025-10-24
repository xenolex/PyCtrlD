"""Utility classes and functions for ControlD API interactions.

This module provides the base endpoint class for API communication, response validation,
and various helper functions for data processing and validation.
"""

from __future__ import annotations

import ipaddress
import re
from pprint import pformat
from typing import TYPE_CHECKING

from requests import Response, Session, exceptions

from pyctrld._core.exceptions import ApiError
from pyctrld._core.logger import logger

if TYPE_CHECKING:
    from typing import Any, Iterable, Optional


class BaseEndpoint:
    """Base class for all ControlD API endpoints.

    This class handles HTTP session management, authentication, and provides
    common methods for GET, POST, PUT, and DELETE requests to the ControlD API.

    Attributes:
        _session: The requests Session object for making HTTP calls.
        _url: The base URL for this endpoint.

    Args:
        token: The API authentication token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the base endpoint with authentication.

        Args:
            token: Bearer token for API authentication.
        """
        self._session = Session()
        self._session.hooks["response"].append(lambda resp, *args, **kwargs: logger.debug(resp.url))

        self._session.headers.update(
            {"Authorization": f"Bearer {token}", "accept": "application/json"}
        )

        self._url = ""

    def __repr__(self) -> str:
        """Return string representation of the endpoint.

        Returns:
            A string showing the class name and URL.
        """
        return f"<{self.__class__.__name__} url={self._url}>"

    def get_raw_response(self, url: str, params: Optional[dict[str, Any]] = None) -> Response:
        """Get raw HTTP response without processing.

        Args:
            url: The URL to request.
            params: Optional query parameters.

        Returns:
            The raw requests.Response object.
        """
        if params is None:
            params = {}
        return self._session.get(url, params=params)

    def _request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[str | dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        """Make an HTTP request and return the response body.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            url: The URL to request.
            params: Optional query parameters.
            data: Optional request body data.
            headers: Optional HTTP headers.

        Returns:
            The 'body' field from the JSON response.

        Raises:
            ApiError: If the response status is not 200.
        """
        response = self._session.request(
            method=method, url=url, params=params, data=data, headers=headers
        )
        check_response(response)
        data = response.json()

        return data["body"]

    def _list(
        self, url: str, model: type, key: str, params: Optional[dict[str, Any]] = None
    ) -> list[Any]:
        """Fetch and validate a list of items from the API.

        Args:
            url: The URL to request.
            model: The Pydantic model class for validation.
            key: The JSON key containing the list of items.
            params: Optional query parameters.

        Returns:
            A list of validated model instances.
        """
        data = self._request("GET", url, params=params)
        return create_list_of_items(model, data[key])

    def _create(
        self, url: str, model: type, key: str, form_data: Optional[dict[str, Any] | str] = None
    ) -> list[Any]:
        """Create a new resource via POST request.

        Args:
            url: The URL to request.
            model: The Pydantic model class for validation.
            key: The JSON key containing the created item(s).
            form_data: Optional form data for the request body.

        Returns:
            A list of validated model instances.
        """
        data = self._request("POST", url, data=form_data)
        return create_list_of_items(model, data[key])

    def _modify(
        self, url: str, model: type, key: str, form_data: Optional[dict[str, Any] | str] = None
    ) -> list[Any]:
        """Modify an existing resource via PUT request.

        Args:
            url: The URL to request.
            model: The Pydantic model class for validation.
            key: The JSON key containing the modified item(s).
            form_data: Optional form data for the request body.

        Returns:
            A list of validated model instances.
        """
        data = self._request("PUT", url, data=form_data)
        return create_list_of_items(model, data[key])

    def _delete(self, url: str, data: Optional[str | dict[str, Any]] = None) -> None:
        """Delete a resource via DELETE request.

        Args:
            url: The URL to request.
            data: Optional data for the request body.
        """
        self._request(
            "DELETE",
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )


def check_response(response: Response) -> None:
    """Validate API response and raise exception on errors.

    Args:
        response: The requests.Response object to validate.

    Raises:
        ApiError: If the response status code is not 200.
    """

    sc_str = f"HTTP Status: {response.status_code}"

    try:
        js = response.json()
    except exceptions.JSONDecodeError:
        js = {}

    msg_str = f" | Message: {js['message']}" if js.get("message") else ""
    logger.debug(sc_str + msg_str)

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
        logger.trace(pformat(item))  # type: ignore
        instance = model.model_validate(item, strict=True)  # type: ignore[attr-defined]
        out_list.append(instance)

    return out_list


def check_via_is_proxy_identifier(via: str | None) -> None:
    """Check that via field contains a valid 3-letter uppercase proxy identifier.

    Args:
        via: The proxy identifier string to validate.

    Raises:
        ValueError: If via is not a 3-letter uppercase string.
    """
    if not all((via is not None, str(via).isupper(), len(str(via)) == 3)):
        raise ValueError(f"via field must be a valid proxy identifier, got: {via}")


def check_via_is_record_or_cname(via: str | None) -> None:
    """Check that via field contains either a valid IPv4 address or domain name.

    Args:
        via: The IP address or domain name to validate.

    Raises:
        ValueError: If via is None, or is neither a valid IPv4 address nor domain name.
    """
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


def check_via_v6_is_aaaa_record(via_v6: str | None) -> None:
    """Check that via_v6 field contains a valid IPv6 address (AAAA record).

    Args:
        via_v6: The IPv6 address to validate.

    Raises:
        ValueError: If via_v6 is not a valid IPv6 address.
    """
    if via_v6 is not None:
        try:
            ipaddress.IPv6Address(via_v6)
        except ipaddress.AddressValueError:
            raise ValueError(f"via_v6 field must be a valid IPv6 address, got: {via_v6}")
