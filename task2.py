from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *

from pyniryo.vision import *
import cv2

robot = connect_to_robot()

vision_position = JointsPosition(-1.5256998217116329, 0.17066572068798735, -0.6855434184041744, -0.0075772503496351895, -1.297840400141045, 0.0016266343776782932)

# robot.move(vision_position)
compressed_img = robot.get_img_compressed()
final_img = uncompress_image(compressed_img)
# write img to folder
cv2.imwrite('vision_images/vision_config4.jpg', final_img)


# cv2.imshow("compressed_img", final_img)
# cv2.waitKey(0)

robot.close_connection()

