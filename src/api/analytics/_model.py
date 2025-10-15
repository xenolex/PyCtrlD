from api._base import ConfiguratedBaseModel


class Level(ConfiguratedBaseModel):
    PK: int
    title: str


class Endpoint(ConfiguratedBaseModel):
    PK: str
    country_code: str
    title: str
