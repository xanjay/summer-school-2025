from utils import *
from pyniryo import *


# ask for destination position from user
destination_pos = BETA_ZONE

def detect_and_pick(robot, destination_pos, object_height=-0.005, workspace="cb"):
    # custom detect and pick function
    print("Detecting object...")
    # 1. Get undistorted image from camera
    undistorted_img = get_undistorted_img_from_camera(robot)
    # 2. Detect object center and angle
    center, cnt_angle = detect_color_objects_using_nyro(undistorted_img)
    # 3. Convert pixel coordinates to relative robot coordinates
    relative_center = relative_pos_from_pixels(undistorted_img, *center)
    # 4. Get world position for robot
    pick_position = robot.get_target_pose_from_rel(workspace, object_height, relative_center[0], relative_center[1],
                                                    cnt_angle)

    # robot.pick_and_place(pick_position, destination_pos)
    # robot.move(pick_position)
    # pick the object
    robot.pick(pick_position)
    print("Detection pick position:", pick_position)
    print("Moving to destination position:", destination_pos)
    robot.place(destination_pos)

def pick_and_place(robot):
    # Move robot automatically to conveyor/workspace pick position
    robot.move(CONVEYER_WORKSPACE_JOINT_POSITION_CENTER)
    print("Detecting and picking object from conveyor belt...")
    detect_and_pick(robot, destination_pos)

def pick_and_place_from_conveyor_to_destination(robot, conveyer_belt):
    # wait till object is detected by infrared sensor
    if robot.digital_read(PinID.DI5) == PinState.LOW:
        robot.stop_conveyor(conveyer_belt)
        robot.wait(2)
        pick_and_place(robot)
        robot.run_conveyor(conveyer_belt, 50, ConveyorDirection.FORWARD)




if __name__ == "__main__":

    # Connect to robot
    robot = connect_to_robot()
    robot.update_tool()
    # set up and run conveyor
    conveyor1 = robot.set_conveyor()

    try:
        robot.run_conveyor(conveyor1, 50, ConveyorDirection.FORWARD)
        while True:
            pick_and_place_from_conveyor_to_destination(robot, conveyor1)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        robot.stop_conveyor(conveyor1)
        robot.close_connection()
    print("Successfully exited.")
