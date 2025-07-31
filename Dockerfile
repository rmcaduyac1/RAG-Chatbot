FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install uv properly
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ src/

# Install dependencies using uv
RUN /root/.local/bin/uv sync --frozen --no-dev

EXPOSE 8000

CMD ["/root/.local/bin/uv", "run", "chainlit", "run", "src/chainlit_app.py", "--host", "0.0.0.0", "--port", "8000"]