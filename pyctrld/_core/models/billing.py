"""Billing models for ControlD API.

This module provides data models for billing-related information including
subscriptions, payments, products, and price points.
"""

from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import ConfiguratedBaseModel, Status


class PricePoint(ConfiguratedBaseModel):
    """Price point configuration for a product.

    Attributes:
        price: Price in USD.
        eur_price: Price in EUR.
        comment: Additional comment or description.
        aud_price: Price in AUD.
        duration: Duration in days for this price point.
        already_billed: Amount already billed.
        cad_stripe_id: Stripe ID for CAD currency.
        type: Type of price point.
        product_id: Associated product identifier.
        jpy_price: Price in JPY.
        gbp_price: Price in GBP.
        jpy_stripe_id: Stripe ID for JPY currency.
        cad_price: Price in CAD.
        eur_stripe_id: Stripe ID for EUR currency.
        chf_stripe_id: Stripe ID for CHF currency.
        stripe_id: Primary Stripe ID.
        aud_stripe_id: Stripe ID for AUD currency.
        gbp_stripe_id: Stripe ID for GBP currency.
        chf_price: Price in CHF.
        PK: Primary key (unique identifier).
    """

    price: float
    eur_price: float
    comment: str
    aud_price: float
    duration: int
    already_billed: int
    cad_stripe_id: str
    type: str
    product_id: int
    jpy_price: float
    gbp_price: float
    jpy_stripe_id: str
    cad_price: float
    eur_stripe_id: str
    chf_stripe_id: str
    stripe_id: str
    aud_stripe_id: str
    gbp_stripe_id: str
    chf_price: float
    PK: int


class Product(ConfiguratedBaseModel):
    """Product information model.

    Attributes:
        proxy_access: Proxy access level included with product.
        type: Type of product.
        priority: Optional priority level.
        name: Product name.
        PK: Primary key (unique identifier).
    """

    proxy_access: int
    type: str
    priority: Optional[int] = None
    name: str
    PK: int


class ActiveSubscription(ConfiguratedBaseModel):
    """Active subscription details.

    Attributes:
        PK: Primary key (unique identifier).
        amount: Subscription amount.
        method: Payment method used.
        next_bill: Timestamp of next billing date.
        price: Subscription price.
        product: Product identifier.
        started: Start date of subscription.
        state: Current state of subscription.
        status: Subscription status (enabled/disabled).
        user: User identifier.
    """

    PK: str
    amount: float
    method: str
    next_bill: int
    price: float
    product: int
    started: str
    state: str
    status: Status
    user: str


class Subscription(ConfiguratedBaseModel):
    """Subscription model with full details.

    Attributes:
        price: Subscription price.
        started: Start date of subscription.
        amount: Subscription amount.
        method: Payment method used.
        state: Current state of subscription.
        product: Associated Product object.
        user: User identifier.
        next_bill: Timestamp of next billing date.
        PK: Primary key (unique identifier).
        status: Subscription status (enabled/disabled).
        currency: Currency code for the subscription.
        currency_amount: Amount in the specified currency.
        next_rebill_date: Date string for next rebill.
    """

    price: float
    started: str
    amount: float
    method: str
    state: str
    product: Product
    user: str
    next_bill: int
    PK: str
    status: Status
    currency: str
    currency_amount: float
    next_rebill_date: str


class ActiveProduct(ConfiguratedBaseModel):
    """Active product with subscription details.

    Attributes:
        proxy_access: Proxy access level included.
        type: Type of product.
        expiry: Expiration date string.
        name: Product name.
        PK: Primary key (unique identifier).
        price: Associated PricePoint object.
        subscription: Associated ActiveSubscription object.
    """

    proxy_access: int
    type: str
    expiry: str
    name: str
    PK: int
    price: PricePoint
    subscription: ActiveSubscription


class Payment(ConfiguratedBaseModel):
    """Payment transaction record.

    Attributes:
        method: Payment method used.
        sub_id: Subscription identifier.
        date: Payment date string.
        amount: Payment amount.
        fingerprint: Payment fingerprint/identifier.
        tx_id: Transaction ID.
        currency: Currency code.
        balance: Account balance after payment.
        user: User identifier.
        product: Associated Product object.
        price_point: Associated PricePoint object.
        ts: Timestamp of payment.
        PK: Primary key (unique identifier).
        tx_status: Transaction status code.
        tx_refunded: Refund status code.
        currency_amount: Amount in the specified currency.
    """

    method: str
    sub_id: str
    date: str
    amount: float
    fingerprint: str
    tx_id: str
    currency: str
    balance: float
    user: str
    product: Product
    price_point: PricePoint
    ts: int
    PK: str
    tx_status: int
    tx_refunded: int
    currency_amount: float
