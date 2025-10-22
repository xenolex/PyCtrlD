from __future__ import annotations

import sys

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api._core.logger import logger
from api._core.models.billing import (
    ActiveProduct,
    ActiveSubscription,
    Payment,
    PricePoint,
    Product,
    Subscription,
)
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.billing import BillingEndpoint
from tests.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")
test_device_id = os.getenv("TEST_DEVICE_ID", "")
test_device_id2 = os.getenv("TEST_DEVICE_ID2", "")


class TestBillingEndpoint:
    """Test the BillingEndpoint class."""

    api = BillingEndpoint(token)

    def test_payments(self):
        check_api_list_endpoint(self.api, Payment, method_name="payments")

    def test_subscriptions(self):
        check_api_list_endpoint(self.api, Subscription, method_name="subscriptions")

    def test_active_products(self):
        check_api_list_endpoint(self.api, ActiveProduct, method_name="active_products")


def test_payments_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.BILLING + "/payments")

    data = response.json()
    items = data["body"]["payments"]
    for payment in items:
        logger.info(payment)
        for key in payment:
            check_key_in_model(key, Payment)
            if key == "product" and payment[key] is not None:
                for p_key in payment[key]:
                    check_key_in_model(p_key, Product)
            if key == "price_point" and payment[key] is not None:
                for pp_key in payment[key]:
                    check_key_in_model(pp_key, PricePoint)


def test_subscriptions_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.BILLING + "/subscriptions")

    data = response.json()
    items = data["body"]["subscriptions"]
    for subscription in items:
        logger.info(subscription)
        for key in subscription:
            check_key_in_model(key, Subscription)
            if key == "product" and subscription[key] is not None:
                for p_key in subscription[key]:
                    check_key_in_model(p_key, Product)


def test_active_products_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.BILLING + "/products")

    data = response.json()
    items = data["body"]["products"]
    for product in items:
        logger.info(product)
        for key in product:
            check_key_in_model(key, ActiveProduct)
            if key == "price_point" and product[key] is not None:
                for pp_key in product[key]:
                    check_key_in_model(pp_key, PricePoint)
            if key == "subscription" and product[key] is not None:
                for s_key in product[key]:
                    check_key_in_model(s_key, ActiveSubscription)
