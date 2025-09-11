import os

import streamlit as st
from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
# from chat_sql.tools import run_sql, run_db_query, plot_fig
from langchain_core.messages import SystemMessage, AIMessage

from utils_llm import detect_objects_with_world_position, create_ollama_client
from dotenv import load_dotenv
load_dotenv()

# config = dotenv_values(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

from utils import encode_image
encoded_img = encode_image(r"vision_images/vision_config1.jpg")

AVAILABLE_TOOLS = {"detect_objects": detect_objects_with_world_position,
                   "create_llm_client": create_ollama_client}


def get_model():
    # initialize openai llm
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        max_retries=2,
        api_key=OPENAI_API_KEY,
    )
    # add function call
    llm_with_tools = llm.bind_tools(list(AVAILABLE_TOOLS.values()))
    return llm



def make_tool_calls(ai_tool_calls):
    plots = []
    tool_messages = []

    for tool_call in ai_tool_calls:
        selected_tool = AVAILABLE_TOOLS[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])

        # this tool returns artifacts along with message
        if tool_call["name"] == "plot_fig":
            tool_message = ToolMessage(
                content=tool_output[0], tool_call_id=tool_call["id"]
            )
            plots.append(tool_output[-1])
        else:
            tool_message = ToolMessage(
                content=tool_output, tool_call_id=tool_call["id"]
            )
        tool_messages.append(tool_message)
    return tool_messages, plots


def run_model(messages, model, artifacts=None):
    # call model
    ai_msg = model.invoke(messages)
    if artifacts:
        # recreate AI message with added plots
        ai_msg = AIMessage(ai_msg.content, plots=artifacts)

    messages.append(ai_msg)
    # make tool calls (if any)
    if len(ai_tool_calls := ai_msg.tool_calls):
        tool_messages, plots = make_tool_calls(ai_tool_calls)
        return run_model(messages + tool_messages, model, artifacts=plots)

    return messages


def initialize_assistant():
    messages = []
    system_message = """
System Prompt: Niryo Robot Assistant
You are a highly capable assistant designed to control and interact with a Niryo robot. You have access to all functions from the tasks in this codebase as callable tools. 
Your primary role is to help users operate the robot, automate tasks, and provide guidance on robot usage, vision, and manipulation.

Capabilities:
You can call any function from the codebase (task1.py, task2.py, ..., task6_2.py, utils.py, utils_llm.py, etc.) as a tool to perform actions or retrieve information.
You can process images, detect objects, move the robot, pick and place items, and interact with the robot’s vision system.
You can answer questions, provide step-by-step instructions, and automate workflows involving the Niryo robot.

Instructions:
Always use the available functions as tools to perform actions. Do not generate code unless explicitly requested.
Respond concisely and clearly, focusing on solving the user’s request using the robot and available functions.
If a user asks for a robot action (e.g., move, pick, place, detect), use the relevant function(s) to execute the task.
If a user asks for information or troubleshooting, use diagnostic or utility functions to gather and present the required data.
If a user asks for a workflow, break it down into steps and execute each using the appropriate tools.
If you encounter an error or need more information, ask for clarification or suggest possible solutions using available functions.

Safety and Best Practices:
Always confirm the robot’s state before performing actions.
Handle errors gracefully and provide informative feedback.
Do not perform any unsafe or destructive actions.
Respect user privacy and workspace integrity.

Example Interactions:
“Move the robot to the vision board.” → Use move_robot_to_vision_board(robot)
“Detect and pick up the red cube.” → Use vision and pick functions to locate and pick the object.
“Show me the current camera image.” → Use get_undistorted_img_from_camera(robot) and display or encode the image.
You are always ready to assist with any Niryo robot task using the full suite of functions in this codebase.
    """

    messages.append(
        SystemMessage(content=system_message)
    )  # noqa: E501

    # model init call
    chain = get_model()
    ai_msg = chain.invoke(messages)
    messages.append(ai_msg)
    return chain, messages

def display_chat_messages(chat_messages):
    for message in chat_messages:
        if message.type in ("ai", "human") and len(message.content):
            with st.chat_message(message.type):
                st.markdown(message.content)

                if hasattr(message, "plots"):
                    for plot in message.plots:
                        st.pyplot(plot)


st.title("Chat with Niriyo Vision Assistant")

if "messages" not in st.session_state:
    st.session_state.chain, st.session_state.messages = initialize_assistant()

display_chat_messages(st.session_state.messages)

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("human"):
        st.markdown(prompt)

    if st.session_state.chain:
        ai_messages = run_model(st.session_state.messages, st.session_state.chain)
        # take only new messages
        new_messages = ai_messages[len(st.session_state.messages) - 1 :]
        display_chat_messages(new_messages)
        st.session_state.messages = ai_messages
    else:
        st.error("Assistant not initialized. Please try again later.")