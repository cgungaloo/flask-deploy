FROM python:3.14-slim
# Set the working directory inside the container
WORKDIR /app

# Copy requirements if you have them (recommended)
# If you don't have a requirements.txt, create one listed below
COPY requirements.txt .

# Install dependencies without caching
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Heroku sets the PORT environment variable automatically
CMD bash -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"