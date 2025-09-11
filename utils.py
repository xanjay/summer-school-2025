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

def get_undistorted_img_from_camera(robot):
    compressed_img = robot.get_img_compressed()
    final_img = uncompress_image(compressed_img)
    undistorted_img = extract_img_workspace(final_img, 1)
    return undistorted_img

def detect_color_objects_using_nyro(img_test, hsv_color=ColorHSV.RED.value):
    img_threshold = threshold_hsv(img_test, *hsv_color)
    img_threshold = morphological_transformations(img_threshold, morpho_type=MorphoType.OPEN,
                                                  kernel_shape=(11, 11), kernel_type=KernelType.ELLIPSE)

    cnt = biggest_contour_finder(img_threshold)
    if not len(cnt):
        raise Exception("No object found")

    cnt_barycenter = get_contour_barycenter(cnt)
    cx, cy = cnt_barycenter
    cnt_angle = get_contour_angle(cnt)
    return (cx, cy), cnt_angle


def move_to_detected_object(robot, object_height=0.1, shape=ObjectShape.SQUARE, color=ColorHSV.RED.value):
    """
    1. Get undistorted image from camera
    2. Detect object center and angle
    3. Convert pixel coordinates to relative robot coordinates
    4. Get world position for robot
    5. Move robot to the detected object position with specified height
    6. Return the world position
    """
    # 1. Get undistorted image from camera
    undistorted_img = get_undistorted_img_from_camera(robot)
    # 2. Detect object center and angle
    center, cnt_angle = detect_color_objects_using_nyro(undistorted_img, hsv_color=color)
    # 3. Convert pixel coordinates to relative robot coordinates
    relative_center = relative_pos_from_pixels(undistorted_img, *center)
    # 4. Get world position for robot
    world_position = robot.get_target_pose_from_rel("vb", object_height, relative_center[0], relative_center[1],
                                                    cnt_angle)
    # world_position.metadata.version=1 # change version to 1 to avoid error
    # world_position.metadata.frame=""
    # 5. Move robot to the detected object position with specified height
    robot.move(world_position)
    return world_position


VISION_BOARD_JOINT_POSITION = JointsPosition(-1.6109277397450201, 0.20853936545626434, -0.7294768463353757,
                                             -0.03672288531946233, -1.290170496201617, 0.026170326983848913)


# conveyer belt position
CONVEYER_WORKSPACE_JOINT_POSITION = JointsPosition(-0.8804027280302735, -0.36562508923081427,
                                                   -0.2446941933014306, 0.1366169437116147, -1.0171219159579725, 1.064675320382428)


BETA_ZONE = JointsPosition(1.9792983074114114, -0.6943683258194581, -0.18561130746291865,
                           0.5262480638345677, -1.2088695144436783, 1.0892190129885981)

CONVEYER_WORKSPACE_JOINT_POSITION_CENTER = JointsPosition(-0.04486474588153211, 0.5645516262780677, -0.6446398820544352,
                                                   0.07372373140830346, -1.6291802503243438, -0.1302957133804865
                                                   )



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def encode_live_image(image):
    return base64.b64encode(image).decode('utf-8')

def move_robot_to_vision_board(robot):
    robot.move(VISION_BOARD_JOINT_POSITION)

