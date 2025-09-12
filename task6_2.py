from utils import *
from pyniryo import *
from task2_5 import move_to_detected_object
from pyniryo.vision import *
import cv2
from utils_llm import detect_objects_with_world_position, create_ollama_client

# Connect to robot
robot = connect_to_robot()
robot.update_tool()

# Move to vision board
robot.move(VISION_BOARD_JOINT_POSITION)
# ask from user for beta zone
beta_zone = BETA_ZONE # destination
# Detect and pick object
print("Detecting object...")

llm_client = create_ollama_client()
pick_position_list = detect_objects_with_world_position(llm_client, robot, object_height=0.0)

for pick_position in pick_position_list:
    print("Picking at position:", pick_position)
    robot.pick(pick_position)
    print("Placing object on conveyor at:", beta_zone)
    robot.place(beta_zone)


robot.close_connection()

