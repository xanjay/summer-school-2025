import os
from typing import List

import httpx
from ollama import Client
from openai import OpenAI
from pydantic import BaseModel
from pyniryo import ObjectColor, ObjectShape, ColorHSV, relative_pos_from_pixels, PoseObject
from utils import get_undistorted_img_from_camera, encode_live_image, detect_color_objects_using_nyro


class DetectedObject(BaseModel):
    color: ObjectColor
    shape: ObjectShape

class DetectedObjectWithHSVColor(BaseModel):
    color: ColorHSV

class DetectedObjectList(BaseModel):
    objects: List[DetectedObjectWithHSVColor]

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

def detect_objects_with_world_position(llm_client, robot, object_height: float=0.1) -> List[PoseObject]:
    """
    1. Get undistorted image from camera
    2. Detect object center and angle
    3. Convert pixel coordinates to relative robot coordinates
    4. Get world position for robot
    5. Move robot to the detected object position with specified height
    6. Return the world position
    """
    world_positions = []
    # 1. Get undistorted image from camera
    undistorted_img = get_undistorted_img_from_camera(robot)
    # find available objects using LLM
    encoded_img = encode_live_image(undistorted_img)
    objects_list: DetectedObjectList = detect_objects(llm_client, encoded_img)

    for object in objects_list.objects:
        # 2. Detect object center and angle
        same_color_objects =  detect_color_objects_using_nyro(undistorted_img, hsv_color=object.color.value)
        for center, cnt_angle in same_color_objects:
            print(f"Detected object: color={object.color}, shape={object.shape}, center={center}, angle={cnt_angle}")
            # 3. Convert pixel coordinates to relative robot coordinates
            relative_center = relative_pos_from_pixels(undistorted_img, *center)
            # 4. Get world position for robot
            world_position = robot.get_target_pose_from_rel("vb", object_height, relative_center[0], relative_center[1],
                                                            cnt_angle)
            # collect all detected objects world positions
            world_positions.append(world_position)
    return world_positions


def get_llm_response(user_message:str):
    return f"Echo from AI: {user_message}"
