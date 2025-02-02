import logging

from faststream.confluent.config import ConfluentConfig

from models.media_channel_tv import MediaChannelTvEnvelope
from models.sales import SaleEnvelope

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

import ssl
from contextlib import asynccontextmanager
from os import environ

from fastapi import FastAPI
from faststream.security import SASLPlaintext

from models.media_channel_radio import MediaChannelRadioEnvelope
from services.media_service import MediaProcessService

import polars as pl


from faststream.confluent import KafkaBroker, KafkaRouter, KafkaRoute


def strtobool(val: str) -> bool:
    val = val.lower()
    if val in ("y", "yes", "true", "t", "on", "1"):
        return True
    elif val in ("n", "no", "false", "f", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value: {val}")


KAFKA_BROKERS = environ.get("KAFKA_BROKERS")
KAFKA_SASL_AUTH_ENABLED = strtobool(environ.get("KAFKA_SASL_AUTH_ENABLED", "True"))
KAFKA_SASL_USER = environ.get("KAFKA_SASL_USER")
KAFKA_SASL_PASSWORD = environ.get("KAFKA_SASL_PASSWORD")

ssl_context = ssl.create_default_context()
security = None
if KAFKA_SASL_AUTH_ENABLED:
    security = SASLPlaintext(
        username=KAFKA_SASL_USER, password=KAFKA_SASL_PASSWORD, use_ssl=True
    )

kafka_config = {
        "api.version.request": "true",
        "broker.version.fallback": "0.10.0.0",
        "api.version.fallback.ms": 0,
        "client.id": "media-channels-client",
        "group.id": "media-channels-group",
        "auto.offset.reset": "earliest",
    }

broker = KafkaBroker(
    bootstrap_servers=KAFKA_BROKERS,
    security=security,
    config=ConfluentConfig(kafka_config)
)

TOPIC_MEDIA_RADIO = "media-radio-test"
TOPIC_MEDIA_TV = "media-tv-test"
TOPIC_SALE = "sale-test"

async def handle_media_radio_event(event: MediaChannelRadioEnvelope):
    logger.info(event)
    df = pl.from_dict(event.model_dump())
    df = df.with_columns(pl.all().fill_null("NULL"))
    print(event)
    logger.info(df)
    table_path = "lakehouse/bronze/media_radio"
    (
        df.write_delta(
            target=table_path,
            mode="append",
        )
    )
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
    print(event)
    logger.info(df)
    table_path = "lakehouse/bronze/media_tv"
    (
        df.write_delta(
            target=table_path,
            mode="append",
        )
    )
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
    print(event)
    logger.info(df)
    table_path = "lakehouse/bronze/sale"
    (
        df.write_delta(
            target=table_path,
            mode="append",
        )
    )
    logger.info("Delta lake written: sale table")


router_sale = KafkaRouter(
    handlers=(
        KafkaRoute(
            handle_media_tv_event,
            TOPIC_MEDIA_TV,
        ),
    )
)

broker.include_routers(router_media_radio, router_media_tv, router_sale)

# BATCH PROCESSING
#
# @broker.subscriber(TOPIC_RADIO, batch=True)  # topic name
# async def handle_msg(payloads: List[MediaBaseEnvelopeWrapper], message: KafkaMessage):
#     for radio_message, raw_message in zip(payloads, list(message.raw_message)):
#         logging.INFO(radio_message)
#         process_content(radio_message)
#


class MediaProcessApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_processor_service: MediaProcessService = None


@asynccontextmanager
async def lifespan(_app: MediaProcessApp):
    await broker.start()
    _app.media_processor_service = MediaProcessService()

    yield

    await broker.close()


app = MediaProcessApp(
    title="MediaProcessService",
    description="MediaProcessService",
    version="0.0.1",
    contact="Me",
    lifespan=lifespan,
)
