# Use a slim Python base image for smaller size
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock .envrc ./

# Install Poetry
RUN pip install --no-cache-dir poetry

#RUN source .envrc

# Set up Poetry's virtual environment (optional but recommended)
RUN poetry config virtualenvs.create true --directory .venv
RUN poetry install --only main --no-ansi --no-interaction --no-root

# Copy the application code
COPY app/ app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Use Uvicorn as the ASGI server.  Adjust if you use a different one.
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]