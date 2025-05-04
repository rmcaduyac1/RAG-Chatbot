FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN poetry config virtualenvs.create true && poetry config virtualenvs.in-project true
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

CMD ["poetry", "run", "chainlit", "run", "src/chainlit_app.py", "--host", "0.0.0.0", "--port", "8000"]
