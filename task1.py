from pyniryo import *
from pyniryo import NiryoRobot

# task 1.1
robot = NiryoRobot("169.254.200.200")
robot.calibrate_auto()
robot.close_connection()

