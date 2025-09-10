from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()
# move to vision position
vision_position = JointsPosition(-1.5256998217116329, 0.17066572068798735, -0.6855434184041744, -0.0075772503496351895, -1.297840400141045, 0.0016266343776782932)
# vision_position = get_joints_position_from_free_move(robot)
robot.move(vision_position)


robot.move_to_object("msm", 0.05, ObjectShape.SQUARE, ObjectColor.RED)
robot.vision_pick()
robot.place()

robot.close_connection()