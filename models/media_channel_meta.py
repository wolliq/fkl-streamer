import datetime

from pydantic import BaseModel, field_serializer


class MediaChannelMeta(BaseModel):
    """
    Class representing media channel Meta
    """

    brand: str
    sub_brand: str
    campaign_name: str
    start_date: datetime

    @field_serializer("start_date")
    def serialize_dt(self, dt: datetime):
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
