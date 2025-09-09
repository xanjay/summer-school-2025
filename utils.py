from pyniryo import *

robot = NiryoRobot("169.254.200.200")

robot.calibrate_auto()

robot.close_connection()

# def main():

