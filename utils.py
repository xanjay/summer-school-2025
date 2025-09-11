import base64
from pyniryo import *


def connect_to_robot():
    robot = NiryoRobot("169.254.200.200")
    robot.calibrate_auto()  # calibrate
    return robot


def get_position_from_free_move(robot):
    try:
        input("Press enter to get position")
        return robot.get_pose()
    except KeyboardInterrupt:
        print("Keyboard interrupt")


def get_joints_position_from_free_move(robot):
    try:
        input("Press enter to get joints position")
        return robot.get_joints()
    except KeyboardInterrupt:
        print("Keyboard interrupt")


VISION_BOARD_JOINT_POSITION = JointsPosition(-1.5941865415598904, 0.30246600448159117, -0.8006792984997363,
                                             0.013898480680763825, -1.2947724385652744, -0.0014413271980928677)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')