import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from configs.config_postgres import DB_URL_CHAINLIT

INIT_CHAINLIT_DATA_LAYER = (
    """
    CREATE TABLE IF NOT EXISTS users (
        "id" UUID PRIMARY KEY,
        "identifier" TEXT NOT NULL UNIQUE,
        "metadata" JSONB NOT NULL,
        "createdAt" TEXT
    );

    CREATE TABLE IF NOT EXISTS threads (
        "id" UUID PRIMARY KEY,
        "createdAt" TEXT,
        "name" TEXT,
        "userId" UUID,
        "userIdentifier" TEXT,
        "tags" TEXT[],
        "metadata" JSONB,
        FOREIGN KEY ("userId") REFERENCES users("id") ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS steps (
        "id" UUID PRIMARY KEY,
        "name" TEXT NOT NULL,
        "type" TEXT NOT NULL,
        "threadId" UUID NOT NULL,
        "parentId" UUID,
        "disableFeedback" BOOLEAN NOT NULL DEFAULT FALSE, -- Set default value
        "streaming" BOOLEAN NOT NULL DEFAULT FALSE,       -- Set default value
        "waitForAnswer" BOOLEAN DEFAULT FALSE,            -- Optional default value
        "isError" BOOLEAN DEFAULT FALSE,                  -- Optional default value
        "metadata" JSONB,
        "tags" TEXT[],
        "input" TEXT,
        "output" TEXT,
        "createdAt" TEXT,
        "start" TEXT,
        "end" TEXT,
        "generation" JSONB,
        "showInput" TEXT,
        "language" TEXT,
        "indent" INT
    );

    CREATE TABLE IF NOT EXISTS elements (
        "id" UUID PRIMARY KEY,
        "threadId" UUID,
        "type" TEXT,
        "url" TEXT,
        "chainlitKey" TEXT,
        "name" TEXT NOT NULL,
        "display" TEXT,
        "objectKey" TEXT,
        "size" TEXT,
        "page" INT,
        "language" TEXT,
        "forId" UUID,
        "mime" TEXT
    );

    CREATE TABLE IF NOT EXISTS feedbacks (
        "id" UUID PRIMARY KEY,
        "forId" UUID NOT NULL,
        "threadId" UUID NOT NULL,
        "value" INT NOT NULL,
        "comment" TEXT
    );
    """
)

async def setup_database_async(conninfo: str):
    # Create an async engine (ensure your DB_URL_CHAINLIT starts with something like "postgresql+asyncpg://")
    engine = create_async_engine(conninfo)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    statements = [
        stmt.strip() for stmt in INIT_CHAINLIT_DATA_LAYER.strip().split(";")
        if stmt.strip()
    ]

    async with async_session() as session:
        try:
            for stmt in statements:
                await session.execute(text(stmt))
            await session.commit()
            print("Database schema has been initialized successfully, or it already exists.")
        except Exception as e:
            await session.rollback()
            print(f"Error during table creation: {e}")
    await engine.dispose()

def setup_database(conninfo: str):
    asyncio.run(setup_database_async(conninfo))

def init_data_layer():
    """
    Initialize the data layer with connection information.
    """
    _conninfo = DB_URL_CHAINLIT
    # Run async table creation
    setup_database(_conninfo)
    
    # Initialize the data layer
    data_layer = SQLAlchemyDataLayer(conninfo=_conninfo)
    return data_layer
