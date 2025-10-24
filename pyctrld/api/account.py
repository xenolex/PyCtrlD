"""Account endpoint for ControlD API.

This module provides access to account-related functionality including
retrieving user data and account information.
"""

from __future__ import annotations

from pyctrld._core.models.account import UserData
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class AccountEndpoint(BaseEndpoint):
    """Endpoint for managing account and user information.

    This endpoint provides methods to retrieve account data for the
    authenticated user.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Account endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.ACCOUNT

    def user_data(self) -> UserData:
        """Retrieve user account data.

        Fetches detailed information about the authenticated user's account,
        including status, email, proxy access, and other account settings.

        Returns:
            UserData object containing account information.

        Reference:
            https://docs.controld.com/reference/get_users
        """
        data = self._request(method="GET", url=self._url)
        return UserData.model_validate(data, strict=True)
