import chainlit as cl
import chainlit.data as cl_data
from chainlit.types import ThreadDict

from agents.persistence_layer import init_data_layer
from agents.service import chatbot_output

# Initialize persistence layer
cl_data._data_layer = init_data_layer()

def get_current_thread_id() -> str:
    """
    Get the current chainlit thread id
    """
    return cl.context.session.thread_id

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> bool:
    """
    Authenticate the user with a username and password.
    """
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier = "admin", metadata = {"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.on_chat_start
async def on_chat_start():
    """
    Starts the chat session.
    """
    return "Welcome to the Medical, Hazard, and Solid Waste Chatbot!"

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """
    Resumes the chat session.
    """
    thread_id = thread.get("id")
    print(f"Resuming chat for thread ID: {thread_id}")

@cl.on_message
async def on_message(message: cl.Message):
    thread_id = get_current_thread_id()
    
    # Remove the introductory message
    introductory_message = cl.user_session.get("introductory_message")
    if introductory_message:
        await introductory_message.remove()

    # Initialize consolidated message for streaming
    consolitated_message = cl.Message(content = "")
    await consolitated_message.send()

    print(f"Received message from user: {message.content}")
    print(f"Starting chatbot logic for thread: {thread_id}")

    # Call the chatbot output function
    bot_response = await chatbot_output(session_id = thread_id, message = message.content)
    
    # Update the consolidated message with the bot response
    await cl.Message(bot_response).send()