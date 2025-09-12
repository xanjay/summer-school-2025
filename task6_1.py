from utils import *
from pyniryo import *


from pyniryo.vision import *
import cv2

from utils_llm import create_openai_client, detect_object_openai

robot = connect_to_robot()
# update tool
robot.update_tool()


move_robot_to_vision_board(robot)

# ask destination position from user
destination_pos = CONVEYER_WORKSPACE_JOINT_POSITION

print("Detecting object...")
undistorted_img = get_undistorted_img_from_camera(robot)
encoded_img = encode_live_image(undistorted_img)

# encoded_img = encode_image(r"vision_images/vision_config1.jpg")

openai_client = create_openai_client()

detected_object = detect_object_openai(openai_client, encoded_img)
print("LLM detected object:", detected_object)
# detect and pick the object
obj_found, shape_ret, color_ret = robot.vision_pick("vb",
                                                    height_offset=-0.001,
                                                    shape=detected_object.shape,
                                                    color=detected_object.color)

print("Detection pick result:", obj_found, shape_ret, color_ret)
print("Moving to destination position:", destination_pos)
robot.place(destination_pos)

robot.close_connection()
