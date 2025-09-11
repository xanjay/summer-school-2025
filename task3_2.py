from utils import *
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()
# update tool
robot.update_tool()


def move_robot_to_vision_board(robot):
    robot.move(VISION_BOARD_JOINT_POSITION)

move_robot_to_vision_board(robot)

# ask destination position from user
destination_pos = CONVEYER_WORKSPACE_JOINT_POSITION

move_robot_to_vision_board(robot)
print("Detecting object...")
# detect object and move to it
object_shape = ObjectShape.SQUARE
object_color = ObjectColor.RED
# detect and pick the object
obj_found, shape_ret, color_ret = robot.vision_pick("vb",
                                                    height_offset=0.01,
                                                    shape=object_shape,
                                                    color=object_color)

print("Detection pick result:", obj_found, shape_ret, color_ret)
print("Moving to destination position:", destination_pos)
robot.place(destination_pos)

robot.close_connection()
