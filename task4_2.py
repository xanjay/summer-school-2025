from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()

conveyor = robot.set_conveyor()

robot.run_conveyor(conveyor, 10, ConveyorDirection.FORWARD)

while True:
    if robot.digital_read(PinID.DI5) == PinState.LOW:
        break

robot.stop_conveyor(conveyor)
robot.unset_conveyor(conveyor)

robot.close_connection()