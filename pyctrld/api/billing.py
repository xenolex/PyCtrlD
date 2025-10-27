"""Billing endpoint for ControlD API.

This module provides access to billing-related functionality including
payments history, subscriptions, and active products.
"""

from __future__ import annotations

from pyctrld._core.models.billing import ActiveProduct, Payment, Subscription
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class BillingEndpoint(BaseEndpoint):
    """Endpoint for managing billing and subscription information.

    This endpoint provides methods to retrieve payment history, subscription
    details, and active product information for the ControlD account.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Billing endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.BILLING

    def payments(self) -> list[Payment]:
        """Returns billing history of all payments made.

        Retrieves the complete payment history for the account, including
        all past transactions and payments.

        Returns:
            A list of Payment objects representing payment history.

        Reference:
            https://docs.controld.com/reference/get_billing-payments
        """

        return self._list(url=self._url + "/payments", model=Payment, key="payments")

    def subscriptions(self) -> list[Subscription]:
        """Returns all active and canceled subscriptions associated with an account.

        Retrieves all subscriptions for the account, including both currently
        active subscriptions and those that have been canceled.

        Returns:
            A list of Subscription objects representing account subscriptions.

        Reference:
            https://docs.controld.com/reference/get_billing-subscriptions
        """

        return self._list(url=self._url + "/subscriptions", model=Subscription, key="subscriptions")

    def active_products(self) -> list[ActiveProduct]:
        """Returns all products currently activated on an account.

        Retrieves the list of products that are currently active and available
        for use on the account.

        Returns:
            A list of ActiveProduct objects representing active products.

        Reference:
            https://docs.controld.com/reference/get_billing-products
        """

        return self._list(url=self._url + "/products", model=ActiveProduct, key="products")
