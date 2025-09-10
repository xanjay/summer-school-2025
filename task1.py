from pyniryo import *
from pyniryo import NiryoRobot
from utils import connect_to_robot, get_position_from_free_move, get_joints_position_from_free_move

# task 1.1
# connect the robot
robot = connect_to_robot()


# task 1.2
# robot.led_ring_flashing([15, 50, 255], iterations=10, wait=True)
# robot.led_ring_snake([250, 0, 55], iterations=10, wait=True)

#task 1.3: get the current position of robot
# get_position_from_free_move(robot)


# task 1.4: first move
# robot.wait(60) # todo: remove comment
#  make free move and test
# robot.move_to_home_pose()

# task 1.5: move the robot between two positions
# position1 = get_position_from_free_move(robot)
# position2 = get_position_from_free_move(robot)

# for i in range(10):
#     robot.move(position1)
#     robot.wait(1) # wait 1 sec
#     robot.move(position2)

# task 1.6: draw s square in the air

joint_position = get_joints_position_from_free_move(robot)

# moves by 0.4 radians
jointPosition1 = JointsPosition(0.060148224552462715, 0.1464265880362901, -0.6734238520783258, -0.012179192713292153, -9.265358979293481e-05, 0.0016266343776782932)
jointPosition2 = JointsPosition(0.060148224552462715, 0.5464265880362901, -0.6734238520783258, -0.012179192713292153, -9.265358979293481e-05, 0.0016266343776782932)
jointPosition3 = JointsPosition(0.460148224552462715, 0.5464265880362901, -0.6734238520783258, -0.012179192713292153, -9.265358979293481e-05, 0.0016266343776782932)
jointPosition4 = JointsPosition(0.460148224552462715, 0.1464265880362901, -0.6734238520783258, -0.012179192713292153, -9.265358979293481e-05, 0.0016266343776782932)

for i in range(2):
    print("move to position 1")
    robot.move(jointPosition1)
    print("move to position 2")
    robot.move(jointPosition2)
    print("move to position 3")
    robot.move(jointPosition3)
    print("move to position 4")
    robot.move(jointPosition4)

print("end last square")
robot.move(jointPosition1)

exit()
# task 1.7:
robot.update_tool()
# moves by 0.4 radians
jointPosition1 = JointsPosition(0.060148224552462715, 0.1464265880362901, -0.6734238520783258, -0.012179192713292153,
                                -9.265358979293481e-05, 0.0016266343776782932)
jointPosition2 = JointsPosition(0.060148224552462715, 0.5464265880362901, -0.6734238520783258, -0.012179192713292153,
                                -9.265358979293481e-05, 0.0016266343776782932)
jointPosition3 = JointsPosition(0.460148224552462715, 0.5464265880362901, -0.6734238520783258, -0.012179192713292153,
                                -9.265358979293481e-05, 0.0016266343776782932)
jointPosition4 = JointsPosition(0.460148224552462715, 0.1464265880362901, -0.6734238520783258, -0.012179192713292153,
                                -9.265358979293481e-05, 0.0016266343776782932)

for i in range(2):
    print("move to position 1")
    robot.move(jointPosition1); robot.grasp_with_tool()
    print("move to position 2")
    robot.move(jointPosition2); robot.release_with_tool()
    print("move to position 3")
    robot.move(jointPosition3); robot.grasp_with_tool()
    print("move to position 4")
    robot.move(jointPosition4); robot.release_with_tool()

print("end last square")
robot.move(jointPosition1); robot.grasp_with_tool()

# disconnect from robot
robot.close_connection()