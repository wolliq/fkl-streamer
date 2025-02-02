import logging

import polars as pl
from faststream.confluent import KafkaRouter, KafkaRoute

from app.constants import TOPIC_MEDIA_RADIO, TOPIC_MEDIA_TV, TOPIC_SALE
from models.media_channel_tv import MediaChannelTvEnvelope
from models.sales import SaleEnvelope
from models.media_channel_radio import MediaChannelRadioEnvelope

logger = logging.getLogger(__name__)


async def handle_media_radio_event(event: MediaChannelRadioEnvelope):
    logger.info(event)
    df = pl.from_dict(event.model_dump())
    df = df.with_columns(pl.all().fill_null("NULL"))

    logger.info(df.head())
    table_path = "lakehouse/bronze/media_radio"

    df.write_delta(target=table_path, mode="append")

    logger.info("Delta lake written: media_radio table")


router_media_radio = KafkaRouter(
    handlers=(
        KafkaRoute(
            handle_media_radio_event,
            TOPIC_MEDIA_RADIO,
        ),
    )
)


async def handle_media_tv_event(event: MediaChannelTvEnvelope):
    logger.info(event)
    df = pl.from_dict(event.model_dump())
    df = df.with_columns(pl.all().fill_null("NULL"))

    logger.info(df.head())
    table_path = "lakehouse/bronze/media_tv"

    df.write_delta(target=table_path, mode="append")

    logger.info("Delta lake written: media_tv table")


router_media_tv = KafkaRouter(
    handlers=(
        KafkaRoute(
            handle_media_tv_event,
            TOPIC_MEDIA_TV,
        ),
    )
)


async def handle_sale_event(event: SaleEnvelope):
    logger.info(event)
    df = pl.from_dict(event.model_dump())
    df = df.with_columns(pl.all().fill_null("NULL"))

    logger.info(df.head())
    table_path = "lakehouse/bronze/sale"

    df.write_delta(target=table_path, mode="append")
    logger.info("Delta lake written: sale table")


router_sale = KafkaRouter(
    handlers=(
        KafkaRoute(
            handle_media_tv_event,
            TOPIC_SALE,
        ),
    )
)
