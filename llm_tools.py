from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool

from utils import connect_to_robot, VISION_BOARD_JOINT_POSITION, get_undistorted_img_from_camera, encode_live_image, \
    CONVEYER_WORKSPACE_JOINT_POSITION
from utils_llm import DetectedObjectList, detect_object_openai, create_openai_client
from utils_llm import detect_objects_with_world_position

# def run_db_query(sql_query):
#     # function to return result in dict form
#     return db_conn.run(sql_query, fetch="cursor").mappings().all()
#

# pydantic class to define function schema
class RunSQLSchema(BaseModel):
    sql_query: str = Field(description="SQL query string")
    database: str = Field(
        description="database type. This field is optional", default="postgresql"
    )


# pydantic class to define function schema
class PlotFigSchema(BaseModel):
    code: str = Field(
        description="""
    It is python(matplotlib) code. when executed, returns figure object.

    `Code` doesn't have any import statements. For e.g.
    It should just be a definition.
    code = "
        def plot():\n
            arr = np.random.normal(1, 1, size=100)
            fig, ax = plt.subplots()
            ax.hist(arr, bins=20)
            return fig
    "
    """
    )

class DetectObjectsSchema(BaseModel):
    """
    A schema for detecting objects from vision board.
    """
    pass

@tool(
    args_schema=DetectObjectsSchema,)
def detect_objects_from_vision_board():
    """
    A function to detect objects from vision board.
    """
    # Connect to robot
    robot = connect_to_robot()
    robot.update_tool()

    # Move to vision board
    robot.move(VISION_BOARD_JOINT_POSITION)
    # 1. Get undistorted image from camera
    undistorted_img = get_undistorted_img_from_camera(robot)
    # find available objects using LLM
    encoded_img = encode_live_image(undistorted_img)
    llm_client = create_openai_client()
    objects_list: DetectedObjectList = detect_object_openai(llm_client, encoded_img)
    print("Ollama detected objects:", objects_list)
    return str(objects_list)

@tool(
    args_schema=DetectObjectsSchema,)
def pick_and_place_object():
    """
    A function to detect objects from vision board.
    """
    # Connect to robot
    robot = connect_to_robot()
    robot.update_tool()

    beta_zone = CONVEYER_WORKSPACE_JOINT_POSITION  # destination
    # Detect and pick object
    print("Detecting object...")

    llm_client = create_openai_client()
    pick_position_list = detect_objects_with_world_position(llm_client, robot, object_height=0.0)

    for pick_position in pick_position_list:
        print("Picking at position:", pick_position)
        robot.pick(pick_position)
        print("Placing object on conveyor at:", beta_zone)
        robot.place(beta_zone)
