from abc import abstractmethod
import datetime
from typing import Self

from pydantic import BaseModel

####################################################
# Classes for Lakehouse serde
####################################################


class MediaBaseModelLakehouse(BaseModel):
    """
    Class base for lakehouse storage
    """

    week: datetime
    campaign_name: str
    brand: str
    sub_brand: str
    media_channel: str

    class Config:
        arbitrary_types_allowed = True


class SaleBaseModelLakehouse(BaseModel):
    """
    Class base for sales in Lakehouse
    """

    week: datetime
    campaign_name: str
    brand: str
    sub_brand: str
    cost: float
    sales_amount: float
    currency: str
    mmm_model: str

    class Config:
        arbitrary_types_allowed = True


####################################################
# Classes for Kafka serde
####################################################


class MediaBaseEnvelopeWrapper(BaseModel):
    """
    Class base BaseEnvelopeWrapper
    """

    event_uuid: str
    event_ts: int
    event_type: str
    occurred_ts: int | None = None
    channel: str | None = "radio"
    request_origin: str | None = "data-api"
    payload: Self
    prev_payload: Self | None = None

    @staticmethod
    def flatten(data: dict) -> dict:
        """
        Recursively flatten the dictionary and return a flat dict.
        """
        flat_dict = {}

        def _flatten(d, parent_key=''):
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):  # If the value is another dictionary
                    _flatten(v, new_key)
                elif isinstance(v, list):  # If the value is a list (this could also be handled)
                    for idx, item in enumerate(v):
                        _flatten(item, f"{new_key}[{idx}]")
                else:
                    flat_dict[new_key] = v

        _flatten(data)
        return flat_dict

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def get_current_week_monday(self, *args) -> datetime.date:
        pass

    @abstractmethod
    def to_lakehouse(self, *args) -> MediaBaseModelLakehouse:
        pass


class SaleBaseEnvelopeWrapper(BaseModel):
    """
    Class base BaseEnvelopeWrapper
    """

    event_uuid: str
    event_ts: int
    event_type: str
    occurred_ts: int | None = None
    channel: str | None = "sale"
    request_origin: str | None = "data-api"
    payload: Self
    prev_payload: Self | None = None

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def flatten(data: dict) -> dict:
        """
        Recursively flatten the dictionary and return a flat dict.
        """
        flat_dict = {}

        def _flatten(d, parent_key=''):
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):  # If the value is another dictionary
                    _flatten(v, new_key)
                elif isinstance(v, list):  # If the value is a list (this could also be handled)
                    for idx, item in enumerate(v):
                        _flatten(item, f"{new_key}[{idx}]")
                else:
                    flat_dict[new_key] = v

        _flatten(data)
        return flat_dict

    @abstractmethod
    def get_current_week_monday(self, *args) -> datetime.date:
        pass

    @abstractmethod
    def to_lakehouse(self, *args) -> SaleBaseModelLakehouse:
        pass
