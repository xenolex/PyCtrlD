from __future__ import annotations

from pyctrld._core.models.billing import ActiveProduct, Payment, Subscription
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class BillingEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.BILLING

    def payments(self) -> list[Payment]:
        """
        Returns billing history of all payments made.
        Reference:
            https://docs.controld.com/reference/get_billing-payments
        """

        return self._list(url=self._url + "/payments", model=Payment, key="payments")

    def subscriptions(self) -> list[Subscription]:
        """
        Returns all active and canceled subscriptions associated with an account.
        Reference:
            https://docs.controld.com/reference/get_billing-subscriptions
        """

        return self._list(url=self._url + "/subscriptions", model=Subscription, key="subscriptions")

    def active_products(self) -> list[ActiveProduct]:
        """
        Returns all products currently activated on an account.
        Reference:
            https://docs.controld.com/reference/get_billing-products
        """

        return self._list(url=self._url + "/products", model=ActiveProduct, key="products")
