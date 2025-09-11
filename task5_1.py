import os
from openai import OpenAI
from pyniryo import *
from pydantic import BaseModel
from dotenv import load_dotenv

from utils import encode_image

class DetectedObject(BaseModel):
    color: ObjectColor
    shape: ObjectShape

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


img = encode_image(r"C:\Users\machm\PycharmProjects\summer-school-2025\vision_images\vision_config1.jpg")

response = client.responses.parse(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "Find what shape does the red object in the picture have and extract its colod and shape to the DetectedObject."},
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Here is the picture:"},
                {"type": "input_image", "image_url": f"data:image/png;base64,{img}"},
            ],
        },
    ],
    text_format=DetectedObject,
)

event = response.output_parsed

print(event)