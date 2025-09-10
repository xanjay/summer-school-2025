from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()

conveyor1 = robot.set_conveyor()

robot.run_conveyor(conveyor1, 50, ConveyorDirection.FORWARD)

while True:
    if robot.digital_read(PinID.DI5) == PinState.LOW:
        break


print("Debug")
robot.stop_conveyor(conveyor1)
# robot.unset_conveyor(conveyor1)

robot.close_connection()
