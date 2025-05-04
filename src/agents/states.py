from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

class ChatRequest(BaseModel):
    session_id: str
    user_message: str