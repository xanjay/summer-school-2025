from pyniryo import *

def connect_to_robot():
    robot = NiryoRobot("169.254.200.200")
    robot.calibrate_auto() # calibrate
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
