import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.confluent import KafkaBroker
from faststream.confluent.config import ConfluentConfig

from app.constants import KAFKA_CONFIG, KAFKA_BROKERS, SECURITY
from app.service.routers import router_media_radio, router_media_tv, router_sale
from services.media_service import MediaProcessService

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


broker = KafkaBroker(
    bootstrap_servers=KAFKA_BROKERS,
    security=SECURITY,
    config=ConfluentConfig(KAFKA_CONFIG),
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
