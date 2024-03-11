import asyncio
import os
from io import BytesIO

import miniopy_async
from loguru import logger
from miniopy_async import Minio

from ports.outbound import ObjectStorageI, SavedObject


class MinioObjectStorage(ObjectStorageI):

    def __init__(self, host: str, user: str, password: str, bucket: str, max_retries: int, retry_timeout: int):
        self._host = host
        self._client = Minio(
            host[host.find('://') + 3:],
            access_key=user,
            secret_key=password,
            secure=True if "https" in host else False
        )
        self._bucket = bucket
        self._max_retries = max_retries
        self._retry_timeout = retry_timeout

    async def save(self, name: str, obj: bytes) -> SavedObject:
        obj_length = len(obj)
        retry = 0
        is_saved = False
        while retry <= self._max_retries and not is_saved:

            try:
                await self._client.put_object(self._bucket, name, BytesIO(obj), obj_length)
            except (miniopy_async.error.S3Error, BaseException) as e:
                logger.exception(e)
                if isinstance(e, miniopy_async.error.S3Error) and e.code == "NoSuchBucket":
                    raise e
                else:
                    logger.warning(f'[{retry}|{self._max_retries}] retry: data saving failed; '
                                   f'sleep {self._retry_timeout} s and retry')
                    await asyncio.sleep(self._retry_timeout)
            else:
                is_saved = True
            retry += 1

        return SavedObject(url=self._get_object_url(name))

    def _get_object_url(self, name: str):
        return os.path.join(self._host, self._bucket, name).replace("\\", "/")
