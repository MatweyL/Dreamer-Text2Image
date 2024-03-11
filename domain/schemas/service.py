from pydantic import BaseModel


class TextToImageTask(BaseModel):
    text: str
    num_inference_steps: int = 50
    negative_prompt: str = "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, " \
                           "out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, " \
                           "bad anatomy, blurred, watermark, grainy, signature, cut off, draft"
    images_number: int = 1


class GeneratedImage(BaseModel):
    value: bytes
    extension: str
