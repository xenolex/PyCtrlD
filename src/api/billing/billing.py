from api._base import BaseEndpoint, check_response, create_list_of_items
from api.billing._model import ActiveProduct, Payment, Subscription
from api.profiles.constants import Endpoints


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

        url = self._url + "/payments"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Payment, data["body"]["payments"])

    def subscriptions(self) -> list[Subscription]:
        """
        Returns all active and canceled subscriptions associated with an account.
        Reference:
            https://docs.controld.com/reference/get_billing-subscriptions
        """

        url = self._url + "/subscriptions"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Subscription, data["body"]["subscriptions"])

    def active_products(self) -> list[ActiveProduct]:
        """
        Returns all products currently activated on an account.
        Reference:
            https://docs.controld.com/reference/get_billing-products
        """

        url = self._url + "/products"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(ActiveProduct, data["body"]["products"])
