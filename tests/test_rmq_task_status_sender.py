from datetime import datetime
from uuid import uuid4

import pytest

from adapters.outbound.rabbit.producer import RabbitMQProducer
from adapters.outbound.rabbit.task_status_sender import RMQTaskStatusSender
from common.utils import build_rmq_default_connection_url
from domain.schemas.core.enums import TaskStatus
from domain.schemas.core.task import TaskStatusLog, TaskPK


@pytest.mark.asyncio
async def test_send():
    rmq_producer = RabbitMQProducer(build_rmq_default_connection_url(), 5, 5)
    await rmq_producer.start()
    rmq_task_status_sender = RMQTaskStatusSender(rmq_producer, 'task.status.exchange', 'DIRECT', 'task.status.queue')
    await rmq_task_status_sender.send(TaskStatusLog(created_timestamp=datetime.now(),
                                                    task_uid=uuid4(),
                                                    uid=uuid4(), task=TaskPK(uid=uuid4()),
                                                    status=TaskStatus.IN_WORK))
    await rmq_producer.stop()
