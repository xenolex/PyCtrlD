from typing import Optional

from api._base import ConfiguratedBaseModel
from api.profiles.constants import Status


class PricePoint(ConfiguratedBaseModel):
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
    proxy_access: int
    type: str
    priority: Optional[int] = None
    name: str
    PK: int


class ActiveSubscription(ConfiguratedBaseModel):
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
    proxy_access: int
    type: str
    expiry: str
    name: str
    PK: int
    price: PricePoint
    subscription: ActiveSubscription


class Payment(ConfiguratedBaseModel):
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
