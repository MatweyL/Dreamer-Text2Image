from uuid import uuid4

from diffusers import StableDiffusionPipeline

from domain.image_generator import ImageGenerator
from domain.schemas.service import TextToImageTask


def test_generate_image():
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", )
    pipe: StableDiffusionPipeline = pipe.to("cpu")

    image_generator = ImageGenerator(pipe)
    task = TextToImageTask(text='pretty red flower',
                           num_inference_steps=1,
                           images_number=1)
    images = image_generator.generate_image(task)
    assert images

