from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()

# task3.1 pick and place
robot.update_tool()
robot.release_with_tool()

print("get object position")
object_position = get_joints_position_from_free_move(robot)

print("get final position")
final_position = get_joints_position_from_free_move(robot)

robot.pick_and_place(object_position, final_position)

robot.close_connection()


