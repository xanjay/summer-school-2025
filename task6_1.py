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

move_robot_to_vision_board(robot)
print("Detecting object...")

undistorted_img = get_undistorted_img_from_camera(robot)
encoded_img = encode_live_image(undistorted_img)

openai_client = create_openai_client()
detected_object = detect_object_openai(openai_client, encoded_img)

# detect object and move to it
object_shape = ObjectShape.SQUARE
object_color = ObjectColor.RED
# detect and pick the object

open

obj_found, shape_ret, color_ret = robot.vision_pick("vb",
                                                    height_offset=0.01,
                                                    shape=object_shape,
                                                    color=object_color)

print("Detection pick result:", obj_found, shape_ret, color_ret)
print("Moving to destination position:", destination_pos)
robot.place(destination_pos)

robot.close_connection()
