import base64
import os
from typing import List

import httpx
from dotenv import load_dotenv
from ollama import Client
from pydantic import BaseModel
from pyniryo import *

load_dotenv()

def connect_to_robot():
    robot = NiryoRobot("169.254.200.200")
    robot.calibrate_auto()  # calibrate
    return robot


def get_position_from_free_move(robot):
    try:
        input("Press enter to get position")
        return robot.get_pose()
    except KeyboardInterrupt:
        print("Keyboard interrupt")


def get_joints_position_from_free_move(robot):
    try:
        input("Press enter to get joints position")
        return robot.get_joints()
    except KeyboardInterrupt:
        print("Keyboard interrupt")


VISION_BOARD_JOINT_POSITION = JointsPosition(-1.5941865415598904, 0.30246600448159117, -0.8006792984997363,
                                             0.013898480680763825, -1.2947724385652744, -0.0014413271980928677)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class DetectedObject(BaseModel):
    color: ObjectColor
    shape: ObjectShape


class DetectedObjectList(BaseModel):
    objects: List[DetectedObject]

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
                "Do NOT default to 0 unless the object is truly axis-aligned or its circle)"
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