import os

import streamlit as st
from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
# from chat_sql.tools import run_sql, run_db_query, plot_fig
from langchain_core.messages import SystemMessage, AIMessage
from llm_tools import detect_objects_from_vision_board, pick_and_place_object

from utils_llm import detect_objects_with_world_position, create_ollama_client
from dotenv import load_dotenv
load_dotenv()

# config = dotenv_values(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

from utils import encode_image
encoded_img = encode_image(r"vision_images/vision_config1.jpg")

AVAILABLE_TOOLS = {"detect_objects_from_vision_board": detect_objects_from_vision_board,
                   "pick_and_place_object": pick_and_place_object}


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
    return llm_with_tools



def format_tool_output(tool_name, tool_output):
    """
    Format tool output to natural language for user display.
    """
    if tool_name == "detect_objects_from_vision_board":
        if hasattr(tool_output, 'objects'):
            objects = tool_output.objects
        else:
            objects = tool_output
        if not objects:
            return "No objects were detected on the vision board."
        return f"The following objects were detected on the vision board: {objects}"
    # Add more tool formatting as needed
    return str(tool_output)


def make_tool_calls(ai_tool_calls):
    plots = []
    tool_messages = []

    for tool_call in ai_tool_calls:
        selected_tool = AVAILABLE_TOOLS[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])
        formatted_output = format_tool_output(tool_call["name"], tool_output)

        # this tool returns artifacts along with message
        if tool_call["name"] == "plot_fig":
            tool_message = ToolMessage(
                content=formatted_output, tool_call_id=tool_call["id"]
            )
            plots.append(tool_output[-1])
        else:
            tool_message = ToolMessage(
                content=formatted_output, tool_call_id=tool_call["id"]
            )
        tool_messages.append(tool_message)
        print("Tool message:", tool_message)
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
You are a Niryo robot assistant.
 Use only the available tools provided to perform actions or answer questions—do not scan or reference the codebase.
  When you use a tool, always format its output into clear, natural language before responding to the user.
  
  Instructions:
  - do not use tool call before user prompt
  Example tool usage:
  detect_objects_from_vision_board()
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