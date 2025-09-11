import os
from typing import List

import httpx
from ollama import Client
from openai import OpenAI
from pydantic import BaseModel
from pyniryo import ObjectColor, ObjectShape


class DetectedObject(BaseModel):
    color: ObjectColor
    shape: ObjectShape


class DetectedObjectList(BaseModel):
    objects: List[DetectedObject]

def create_openai_client():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client

def create_ollama_client():
    client = Client(
    host=os.getenv("OLLAMA_HOST"),
    auth=httpx.DigestAuth(os.getenv("OLLAMA_USER"), os.getenv("OLLAMA_PASSWORD")),
    )
    return client

def detect_objects(ollama_client, encoded_img):
    """return list DetectedObjectList that is list wrapper around the DetectedObject (each object have color and shape).
        Detects all RED, GREEN, BLUE, YELLOW objects from the image."""

    message = [
        {
            "role": "system",
            "content": (
                "You are a vision analysis assistant. "
                "Identify all objects with RED, BLUE, GREEN, YELLOW color in the image. "
                "Return ONLY a JSON that will be list of objects with the following fields:"
                "shape"
                "color"
                "Do not include explanations or extra text. Only return valid JSON."
            )
        },
        {
            "role": "user",
            "content": "Here is the picture.",
            'images': [encoded_img],
        }
    ]

    # Send the request
    response = ollama_client.chat(
        model="gemma3:27b",
        messages=message,
        format=DetectedObjectList.model_json_schema(),
        options={"temperature": 0}
    )

    detected_objects = DetectedObjectList.model_validate_json(response.message.content)
    return detected_objects

def detect_object_openai(openai_client, encoded_img):
    response = openai_client.responses.parse(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a vision analysis assistant. "
                    "Identify the RED object in the image. "
                    "Return ONLY a JSON object with the following fields:"
                    "shape"
                    "color"
                    "Do not include explanations or extra text. Only return valid JSON."
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Here is the picture:"},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{encoded_img}"},
                ],
            },
        ],
        text_format=DetectedObject,
    )

    event = response.output_parsed
    return event