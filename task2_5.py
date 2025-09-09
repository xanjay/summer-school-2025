from utils import get_position_from_free_move, connect_to_robot, get_joints_position_from_free_move
from pyniryo import *


from pyniryo.vision import *
import cv2

robot = connect_to_robot()

def get_undistorted_img_from_camera(robot):
    compressed_img = robot.get_img_compressed()
    final_img = uncompress_image(compressed_img)
    undistorted_img = extract_img_workspace(final_img, 1)
    return undistorted_img


import cv2
import numpy as np

def detect_color_objects(image, color_name):
    # Define HSV color ranges
    color_ranges = {
        'red': [(np.array([0, 120, 70]), np.array([10, 255, 255])),
                (np.array([170, 120, 70]), np.array([180, 255, 255]))],
        'blue': [(np.array([100, 100, 100]), np.array([120, 255, 255]))],
        'green': [(np.array([220, 100, 100]), np.array([240, 255, 255]))],
        'yellow': [(np.array([15, 150, 150]), np.array([35, 255, 255]))]
    }

    if color_name not in color_ranges:
        raise ValueError(f"Unsupported color: {color_name}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create mask(s)
    masks = [cv2.inRange(hsv, lower, upper) for lower, upper in color_ranges[color_name]]
    mask = masks[0]
    for m in masks[1:]:
        mask = cv2.bitwise_or(mask, m)

    # Apply mask
    result = cv2.bitwise_and(image, image, mask=mask)

    # Optional: Draw contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cv2.drawContours(result, [cnt], 0, (0, 255, 0), 2)

    # Show results
    cv2.imshow('Detected Objects', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_color_objects_using_nyro(img_test, hsv_color=ColorHSV.RED.value):
    img_threshold = threshold_hsv(img_test, *hsv_color)
    img_threshold = morphological_transformations(img_threshold, morpho_type=MorphoType.OPEN,
    kernel_shape=(11, 11), kernel_type=KernelType.ELLIPSE)
    cnt = biggest_contour_finder(img_threshold)
    cnt_barycenter = get_contour_barycenter(cnt)
    cx, cy = cnt_barycenter
    cnt_angle = get_contour_angle(cnt)
    # img_debug = draw_contours(img_threshold, [cnt])
    # img_debug = draw_barycenter(img_debug, cx, cy)
    # img_debug = draw_angle(img_debug, cx, cy, cnt_angle)
    # show_img_and_wait_close("Image with contours, barycenter and angle", img_debug)
    return (cx,cy), cnt_angle


undistorted_img = get_undistorted_img_from_camera(robot)
center, cnt_angle = detect_color_objects_using_nyro(undistorted_img)

relative_center = relative_pos_from_pixels(undistorted_img, *center)
print(relative_center)

robot.close_connection()

# todo