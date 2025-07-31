# 🧠 RAG-Chatbot with Chainlit, Docker, and PostgreSQL

A Retrieval-Augmented Generation (RAG) chatbot built with Python, Chainlit, and PostgreSQL. The chatbot handles queries related to **medical**, **hazardous**, and **solid waste**, and features user authentication, session persistence, and database-backed interactions.

---

## 🚀 Features

- 🗣️ Conversational chatbot powered by Chainlit  
- 🔍 Retrieval-augmented answers using FAQ data  
- 🗃️ PostgreSQL-based data persistence  
- 🔐 Admin login with password authentication  
- 🐳 Fully containerized using Docker & Docker Compose  
- 📂 `.env` support for secure configuration  

---

## 🧰 Tech Stack

- **Frontend**: Chainlit  
- **Backend**: Python 3.11  
- **Database**: PostgreSQL  
- **Containerization**: Docker, Docker Compose  
- **Dependency Management**: uv 

---

## 🛠️ Setup & Run (Local)

1. Create `.env` file (already in `.gitignore`) with:
   ```env
    OPENAI_API_KEY = "<placeholder>"
    PINECONE_API_KEY = "<placeholder>"

    DB_CHATBOT_USER="<placeholder>"
    DB_CHATBOT_PASSWORD="<placeholder>"
    DB_CHATBOT_DB="RAG_CHATBOT"
    DB_URL_CHATBOT="postgresql://<placeholder>:<placeholder>@rag-chatbot-db:5432/RAG_CHATBOT"

    DB_CHAINLIT_USER="<placeholder>"
    DB_CHAINLIT_PASSWORD="<placeholder>"
    DB_CHAINLIT_DB="RAG_CHATBOT_CHAINLIT"
    DB_URL_CHAINLIT="postgresql+asyncpg://<placeholder>:<placeholder>@rag-chatbot-chainlit-db:5432/RAG_CHATBOT_CHAINLIT"

    CHAINLIT_AUTH_SECRET="<placeholder>"

Note, CHAINLIT_AUTH_SECRET can be obtained using the command:
```bash
chainlit create-secret
```

2. Install dependencies using uv and activate venv
```bash
uv install
uv sync
source .venv/bin/activate
```

3. Run the `vectorstore.py` to store the embeddings of the book inside Pinecone
```bash
uv run python -m src.data.vectorstore
```

4. Run the application
```bash
docker compose -f docker-compose.yml up --build
```

5. The login credentials in the chainlit application can be seen in `chainlit_app.py`.