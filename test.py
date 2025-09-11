from utils import *
from pyniryo import *
import numpy as np

from pyniryo.vision import *
import cv2

robot = connect_to_robot()

print(get_joints_position_from_free_move(robot))
