import os

import httpx
from dotenv import load_dotenv
from ollama import Client

from utils import encode_image, DetectedObject

load_dotenv()

client = Client(
    host=os.getenv("OLLAMA_HOST"),
    auth=httpx.DigestAuth(os.getenv("OLLAMA_USER"), os.getenv("OLLAMA_PASSWORD")),
)

img = encode_image(r"vision_images/vision_config1.jpg")

message = [
    {
        "role": "system",
        "content": (
            "You are a vision analysis assistant. "
            "Identify the BLUE object in the image. "
            "Return ONLY a JSON object with the following fields:"
            "position_x: integer (the x coordinate of the object's center pixel)"
            "position_y: integer (the y coordinate of the object's center pixel)"
            "shape"
            "rotation: float (if its square compute the angle of the square relative to the horizontal axis in degrees"
            "Do NOT default to 0 unless the object is truly axis-aligned or its circle)"
            "Do not include explanations or extra text. Only return valid JSON."
        )
    },
    {
        "role": "user",
        "content": "Here is the picture.",
        'images': [img],
    }
]

# Send the request
response = client.chat(
    model="gemma3:27b",
    messages=message,
    format=DetectedObject.model_json_schema(),
    options={"temperature": 0}
)

object_t = DetectedObject.model_validate_json(response.message.content)
print(object_t)
