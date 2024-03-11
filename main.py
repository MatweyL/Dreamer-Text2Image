import asyncio
from asyncio import CancelledError

from diffusers import StableDiffusionPipeline

from adapters.common.converter import StrToPydantic
from adapters.common.settings import rmq_settings
from adapters.inbound.rabbit.consumer import RabbitMQConsumer
from adapters.inbound.rabbit.settings import rmq_consumer_settings
from adapters.outbound.minio.object_storage import MinioObjectStorage
from adapters.outbound.minio.settings import minio_settings
from adapters.outbound.rabbit.producer import RabbitMQProducer
from adapters.outbound.rabbit.settings import task_status_settings, rmq_producer_settings
from adapters.outbound.rabbit.task_status_sender import RMQTaskStatusSender
from common.utils import build_connection_url
from domain.image_generator import ImageGenerator, ImageGeneratorManager
from domain.schemas.core.task import FullTask
from domain.task_data_converter import TaskDataConverter


async def main():
    task_data_converter = TaskDataConverter()
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", )
    pipe: StableDiffusionPipeline = pipe.to("cpu")

    rmq_connection_url = build_connection_url(rmq_settings.protocol, rmq_settings.user, rmq_settings.password,
                                              rmq_settings.host, rmq_settings.port, rmq_settings.virtual_host)
    rabbit_mq_consumer = RabbitMQConsumer(rmq_connection_url,
                                          rmq_consumer_settings.prefetch_count,
                                          rmq_consumer_settings.reconnect_timeout)
    rabbit_mq_producer = RabbitMQProducer(rmq_connection_url,
                                          rmq_producer_settings.reconnect_timeout,
                                          rmq_producer_settings.produce_retries)
    task_status_sender = RMQTaskStatusSender(rabbit_mq_producer,
                                             task_status_settings.exchange_name,
                                             task_status_settings.exchange_type,
                                             task_status_settings.routing_key)
    image_storage = MinioObjectStorage(minio_settings.host,
                                       minio_settings.user,
                                       minio_settings.password,
                                       minio_settings.bucket,
                                       minio_settings.retries,
                                       minio_settings.retry_timeout, )
    image_generator = ImageGenerator(pipe)
    image_generator_manager = ImageGeneratorManager(image_generator, task_status_sender,
                                                    image_storage, task_data_converter)
    converter = StrToPydantic(FullTask)
    await rabbit_mq_consumer.start()
    await rabbit_mq_producer.start()
    await rabbit_mq_consumer.consume_queue(rabbit_mq_consumer.queue_name,
                                           image_generator_manager.generate_image,
                                           converter)
    try:
        await asyncio.Future()
    except CancelledError:
        pass
    await rabbit_mq_consumer.stop()
    await rabbit_mq_producer.stop()


if __name__ == '__main__':
    asyncio.run(main())
