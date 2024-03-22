# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY .venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

# Install any dependencies specified in requirements.txt
RUN /app/.venv/bin/python -m pip freeze > requirements.txt && \
    /app/.venv/bin/python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose port 80 to allow external access
EXPOSE 8000

# Define the command to run the application when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]