from datetime import datetime
from io import BytesIO
from typing import List
from uuid import uuid4

from PIL.Image import Image
from diffusers import StableDiffusionPipeline
from loguru import logger

from domain.schemas.core.enums import TaskStatus
from domain.schemas.core.task import FullTask, TaskStatusLog, FullTaskStatus
from domain.schemas.service import TextToImageTask, GeneratedImage
from domain.task_data_converter import TaskDataConverter
from ports.outbound import TaskStatusSenderI, ObjectStorageI


class ImageGeneratorManager:
    def __init__(self, image_generator: 'ImageGenerator',
                 task_status_sender: TaskStatusSenderI,
                 image_storage: ObjectStorageI,
                 task_data_converter: TaskDataConverter):
        self._image_generator = image_generator
        self._task_status_sender = task_status_sender
        self._image_storage = image_storage
        self._task_data_converter = task_data_converter

    async def generate_image(self, task: FullTask):
        task_status_log = TaskStatusLog(
            task_uid=task.uid,
            created_timestamp=datetime.now(),
            status=TaskStatus.IN_WORK,
        )
        await self._task_status_sender.send(task_status_log)
        text_to_image_task = self._task_data_converter.to_schema(task.input, TextToImageTask)
        try:
            images = self._image_generator.generate_image(text_to_image_task)
        except BaseException as e:
            logger.exception(e)
            task_status_log = TaskStatusLog(
                task_uid=task.uid,
                created_timestamp=datetime.now(),
                status=TaskStatus.ERROR,
            )
            await self._task_status_sender.send(task_status_log)
        else:
            finished_timestamp = datetime.now()
            images_urls = []
            for image in images:
                saved_image = await self._image_storage.save(f'{uuid4().hex}.{image.extension}', image.value)
                images_urls.append(saved_image.url)
            output = self._task_data_converter.to_data(task, is_input=False, images_urls=images_urls)
            task_status_log = FullTaskStatus(
                task_uid=task.uid,
                created_timestamp=finished_timestamp,
                status=TaskStatus.FINISHED,
                output=output,
            )
            await self._task_status_sender.send(task_status_log)


class ImageGenerator:

    def __init__(self, pipeline: StableDiffusionPipeline):
        self._pipeline = pipeline

    def generate_image(self, task: TextToImageTask) -> List[GeneratedImage]:
        result = self._pipeline(prompt=task.text,
                                negative_prompt=task.negative_prompt,
                                num_images_per_prompt=task.images_number,
                                num_inference_steps=task.num_inference_steps,
                                )
        images: List[Image] = result.images
        bytes_images = []
        for image in images:
            image_bytes_io = BytesIO()
            image.save(image_bytes_io, format='PNG')
            bytes_images.append(GeneratedImage(value=image_bytes_io.getvalue(),
                                               extension='png'))
        return bytes_images
