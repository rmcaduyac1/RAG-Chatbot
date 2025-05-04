# Import necessary libraries
import os
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
from typing import List
from agents.agent import init_agent_executor
from configs.config_postgres import DB_URL_CHATBOT, connection_kwargs

# Define database URL
DB_URL = DB_URL_CHATBOT

async def chatbot_output(session_id: str, message: str) -> str:

    async with AsyncConnectionPool(conninfo = DB_URL, max_size = 20, kwargs = connection_kwargs) as pool:
        
        checkpointer = AsyncPostgresSaver(pool)
        
        await checkpointer.setup()
        graph = init_agent_executor(checkpointer)

        configs = {"configurable": {"thread_id": session_id}}

        output = await graph.ainvoke(
            {"messages": {"role": "user", "content": message}}, 
            config = configs,
        )

        return output["messages"][-1].content