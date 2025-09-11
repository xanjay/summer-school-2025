from utils import *
from pyniryo import *
from task2_5 import move_to_detected_object
from pyniryo.vision import *
import cv2

# Connect to robot
robot = connect_to_robot()
robot.update_tool()

# Move to vision board
robot.move(VISION_BOARD_JOINT_POSITION)
# ask from user for conveyor place position
conveyor_place_position = CONVEYER_WORKSPACE_JOINT_POSITION
robot.move(VISION_BOARD_JOINT_POSITION)
# Detect and pick object
print("Detecting object...")
pick_position = move_to_detected_object(robot, object_height=0.0)
robot.pick(pick_position)
print("Detection pick position:", pick_position)

# Place object on conveyor belt (assume conveyor position is known)
print("Placing object on conveyor at:", conveyor_place_position)
robot.place(conveyor_place_position)

# Set up and run conveyor
conveyor1 = robot.set_conveyor()
robot.run_conveyor(conveyor1, 50, ConveyorDirection.FORWARD)
print("Conveyor running...")

# Wait for object to reach infrared sensor
while True:
    if robot.digital_read(PinID.DI5) == PinState.LOW:
        print("Object detected by infrared sensor.")
        break

robot.stop_conveyor(conveyor1)
print("Conveyor stopped.")
robot.close_connection()

