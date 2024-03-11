import pprint
import time

from PIL.Image import Image
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", )
pipe: StableDiffusionPipeline = pipe.to("cpu")

prompt = "red cat sitting on table, realistic photo, simple picture, symbol"
negative_prompt = "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft"
s = time.perf_counter()
result = pipe(prompt,
              negative_prompt=negative_prompt,
              num_images_per_prompt=3,
              num_inference_steps=5)
f = time.perf_counter()
print(type(result))
pprint.pprint(result.images)
print('duration:', f - s)
for i, image in enumerate(result.images):
    image: Image
    image.save(prompt.replace(' ', '_').replace(',', '') + f'_{i}.jpg')
