import asyncio
import json
from typing import Dict

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractExchange
from loguru import logger

from ports.outbound import RabbitMQProducerI


class RabbitMQProducer(RabbitMQProducerI):

    def __init__(self, connection_url: str, reconnect_timeout: int, produce_retries: int):
        self._connection_url = connection_url
        self._reconnect_timeout = reconnect_timeout
        self._produce_retries = produce_retries

        self._connection: AbstractConnection = None
        self._channel: AbstractChannel = None

        self._exchanges: Dict[tuple[str, str], AbstractExchange] = {}

    async def produce(self, data: dict, exchange_name: str, exchange_type: str, routing_key: str, headers: dict):
        try:
            exchange = self._exchanges[(exchange_name, exchange_type)]
        except KeyError:
            exchange = await self._channel.declare_exchange(exchange_name, exchange_type, passive=True)
            self._exchanges[(exchange_name, exchange_type)] = exchange
        message = Message(body=json.dumps(data, default=str).encode('utf-8'), headers=headers)
        retry = 0
        while retry < self._produce_retries:
            retry += 1
            try:
                await exchange.publish(message, routing_key=routing_key)
            except BaseException as e:
                logger.error(f'failed to produce message: {e}; retries: {retry}|{self._produce_retries}')
            else:
                logger.info(f'successfully produced message; retries: {retry}|{self._produce_retries}')
                break

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
