from task2 import vision_position, robot
from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *

from pyniryo.vision import *
import cv2

robot = connect_to_robot()

robot.set_arm_max_velocity(40)

vision_position = JointsPosition(-1.5256998217116329, 0.17066572068798735, -0.6855434184041744, -0.0075772503496351895, -1.297840400141045, 0.0016266343776782932)
# vision_position = get_joints_position_from_free_move(robot)
robot.move(vision_position)

#detected_objects = robot.detect_object("msm", ObjectShape.SQUARE, ObjectColor.RED)
#pose_position = robot.get_target_pose_from_rel("msm", 0.1, detected_objects[1][0], detected_objects[1][1], detected_objects[1][2])
# cv2.imshow("compressed_img", final_img)
# cv2.waitKey(0)
#print(objects)
#print(pose_position)
#pose_joints = robot.inverse_kinematics(pose_position)
robot.move_to_object("msm", 0.05, ObjectShape.SQUARE, ObjectColor.RED)
#robot.move(pose_position)

robot.close_connection()

