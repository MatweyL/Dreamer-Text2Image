from pathlib import Path

import pytest

from adapters.outbound.minio.object_storage import MinioObjectStorage


@pytest.mark.asyncio
async def test_save():
    object_storage = MinioObjectStorage('http://127.0.0.1:9000', 'minio', 'minio123456789', 'videos', 5, 1)
    image = Path(r'C:\Users\Acer\Downloads\ussr_cat.jpg').read_bytes()
    saved_object = await object_storage.save('ussr_cat.jpg', image)
    assert saved_object.url
