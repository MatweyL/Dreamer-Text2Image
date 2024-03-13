import asyncio
from typing import Optional, Callable, Awaitable

from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractIncomingMessage
from loguru import logger

from ports.common import ConverterI, Startable


class RabbitMQConsumer(Startable):

    def __init__(self, connection_url: str, prefetch_count: int = 0, reconnect_timeout: int = 5):
        self._connection_url = connection_url
        self._prefetch_count = prefetch_count
        self._reconnect_timeout = reconnect_timeout
        self._connection: Optional[AbstractConnection] = None
        self._channel: Optional[AbstractChannel] = None

    async def start(self):
        try:
            self._connection = await connect_robust(self._connection_url)
        except BaseException as e:
            logger.warning(f'{self} cannot create connection: {e}; sleep {self._reconnect_timeout} s and retry')
            await asyncio.sleep(self._reconnect_timeout)
            return await self.start()
        else:
            self._channel = await self._connection.channel()
            logger.info(f'{self} started')

    async def stop(self):
        if not self._connection.is_closed:
            await self._connection.close()
            logger.info(f'{self} stopped')
        else:
            logger.info(f'{self} already stopped')

    def _processing_callback_bridge(self, processing_callback: Callable[[dict], Awaitable],
                                    message_converter: ConverterI):

        async def inner(message: AbstractIncomingMessage):
            logger.debug(f'{self} got message')
            try:
                async with message.process():
                    decoded_message = message.body.decode('utf-8')
                    converted_message = message_converter.convert(decoded_message)
                await processing_callback(converted_message)
            except BaseException as e:
                logger.exception(e)
                logger.error(f'{self} failed to process message: {e}')

        return inner

    async def consume_queue(self, queue_name: str, processing_callback: Callable[[dict], Awaitable[bool]],
                            message_converter: ConverterI, **kwargs):
        queue = await self._channel.declare_queue(queue_name, **kwargs)
        await queue.consume(self._processing_callback_bridge(processing_callback, message_converter))
