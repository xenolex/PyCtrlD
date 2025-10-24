"""Custom exceptions for the PyCtrlD library.

This module defines custom exception classes used throughout the ControlD API client
for handling API errors and other exceptional conditions.
"""

from __future__ import annotations

from requests import Response


class ApiError(Exception):
    """Exception raised when the ControlD API returns an error response.

    This exception is raised when an API request fails, providing detailed
    information about the HTTP status code, API error code, and error message
    from the ControlD API response.

    Attributes:
        message: Formatted error message containing HTTP status, error code, and API message.

    Example:
        >>> try:
        ...     api.devices.list_all_devices()
        ... except ApiError as e:
        ...     print(f"API Error: {e}")
        API Error: HTTP Status: 401 | Error Code: 1001 | Message: Invalid token
    """

    def __init__(self, response: Response) -> None:
        """Initialize ApiError with response details.

        Extracts error information from the API response and formats it into
        a comprehensive error message.

        Args:
            response: The HTTP response object from the failed API request.
                Must contain a JSON body with an 'error' field containing
                'code' and 'message' fields.

        Raises:
            KeyError: If the response JSON doesn't contain expected error fields.
            JSONDecodeError: If the response body is not valid JSON.
        """
        data = response.json()["error"]

        message = (
            f"HTTP Status: {response.status_code} | "
            f"Error Code: {data['code']} | Message: {data['message']}"
        )

        super().__init__(message)
