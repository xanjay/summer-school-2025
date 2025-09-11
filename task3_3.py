from utils import *
from pyniryo import *
from task2_5 import move_to_detected_object

from pyniryo.vision import *
import cv2

robot = connect_to_robot()
# update tool
robot.update_tool()


def move_robot_to_vision_board(robot):
    robot.move(VISION_BOARD_JOINT_POSITION)

move_robot_to_vision_board(robot)

# ask destination position from user
destination_pos = get_position_from_free_move(robot)

move_robot_to_vision_board(robot)
print("Detecting object...")
# detect object and move to it
# detect using task2.5
pick_position = move_to_detected_object(robot, object_height=0.0)
# pick the object
robot.pick(pick_position)

print("Detection pick position:", pick_position)
print("Moving to destination position:", destination_pos)
robot.place(destination_pos)

robot.close_connection()

