import os
from openai import OpenAI
from dotenv import load_dotenv

from utils import encode_image, DetectedObject

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


img = encode_image(r"vision_images/vision_config1.jpg")

response = client.responses.parse(
    model="gpt-4o",
    input=[
        {
            "role": "system",
            "content": (
                "You are a vision analysis assistant. "
                "Identify the RED object in the image. "
                "Return ONLY a JSON object with the following fields:"
                "position_x: integer (the x coordinate of the object's center pixel)"
                "position_y: integer (the y coordinate of the object's center pixel)"
                "shape"
                "rotation: float (the angle of rotation of the shape in degrees)"
                "Do not include explanations or extra text. Only return valid JSON."
            )
        },
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