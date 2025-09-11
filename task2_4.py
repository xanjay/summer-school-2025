from utils import *
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()

vision_position = VISION_BOARD_JOINT_POSITION
robot.move(vision_position)
#
# for i in range(100):
#     compressed_img = robot.get_img_compressed()
#     final_img = uncompress_image(compressed_img)
#
#     undistorted_img = extract_img_workspace(final_img, 1)
#
#     cv2.imshow("undistorted_img ", undistorted_img)
#     cv2.waitKey(0)


compressed_img = robot.get_img_compressed()
final_img = uncompress_image(compressed_img)

undistorted_img = extract_img_workspace(final_img, 1)

cv2.imshow("undistorted_img ",undistorted_img)
cv2.waitKey(0)

robot.close_connection()