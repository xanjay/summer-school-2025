from task2 import vision_position, robot
from utils import *
from pyniryo import *

from pyniryo.vision import *
import cv2

robot = connect_to_robot()

# robot.set_arm_max_velocity(40)
# move to vision position
vision_position = VISION_BOARD_JOINT_POSITION
# vision_position = get_joints_position_from_free_move(robot)
robot.move(vision_position)

detected_objects = robot.detect_object("vb", ObjectShape.SQUARE, ObjectColor.RED)
pose_position = robot.get_target_pose_from_rel("vb", 0.05, detected_objects[1][0], detected_objects[1][1],
                                               detected_objects[1][2])
# pose_position.metadata.version = 1  # change version to 1 to avoid error
print(pose_position)
robot.move(pose_position)

# target_pos.metadata.version = 1  # change version to 1 to avoid error
# target_pos.metadata=PoseMetadata.v1(frame="frame")
# cv2.imshow("compressed_img", final_img)
# cv2.waitKey(0)
#print(objects)
#print(pose_position)
#pose_joints = robot.inverse_kinematics(pose_position)
# robot.move_to_object("mss", 0.05, ObjectShape.SQUARE, ObjectColor.RED)

robot.close_connection()

