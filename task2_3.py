from task2 import vision_position, robot
from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *

from pyniryo.vision import *
import cv2

robot = connect_to_robot()

# robot.set_arm_max_velocity(40)
# move to vision position
vision_position = JointsPosition(-1.5256998217116329, 0.17066572068798735, -0.6855434184041744, -0.0075772503496351895, -1.297840400141045, 0.0016266343776782932)
# vision_position = get_joints_position_from_free_move(robot)
robot.move(vision_position)

# detected_objects = robot.detect_object("msm", ObjectShape.SQUARE, ObjectColor.RED)
# pose_position = robot.get_target_pose_from_rel("msm", 0.05, detected_objects[1][0], detected_objects[1][1],
#                                                detected_objects[1][2])
# pose_position.metadata.version = 1  # change version to 1 to avoid error
# print(pose_position)
# robot.move(pose_position, linear=True)

# target_pos.metadata.version = 1  # change version to 1 to avoid error
# target_pos.metadata=PoseMetadata.v1(frame="frame")
input("do free move and press enter")
target_pos = PoseObject(x = -0.0511, y = -0.3089, z = 0.0938, roll = -3.138, pitch = -0.009, yaw = -1.986)
target_pos.metadata.version=1 # change version to 1 to avoid error
robot.move(target_pos)
# cv2.imshow("compressed_img", final_img)
# cv2.waitKey(0)
#print(objects)
#print(pose_position)
#pose_joints = robot.inverse_kinematics(pose_position)
# robot.move_to_object("msm", 0.05, ObjectShape.SQUARE, ObjectColor.RED)

robot.close_connection()

