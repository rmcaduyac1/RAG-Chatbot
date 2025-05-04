from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START
from agents.model import init_chatbot_model
from agents.prompts import SYSTEM_PROMPT
from agents.tools import retriever_tools
from agents.states import State 

def init_agent_executor(checkpoint, tools = retriever_tools(), prompt = SYSTEM_PROMPT, 
                        llm = init_chatbot_model("gpt-4o-mini")):
    
    # Define prompt
    PROMPT = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            MessagesPlaceholder(variable_name = "messages"),
        ]
    )

    # Bind LLM, tool, and prompt
    bind_model = PROMPT | llm.bind_tools(tools)

    # Define chatbot state
    def chatbot(state: State):
        return {"messages": [bind_model.invoke(state["messages"])]}
    
    # Build the graph
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", ToolNode(tools = tools))

    # Add edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")

    # Compile the graph
    graph = graph_builder.compile(checkpointer = checkpoint)

    return graph