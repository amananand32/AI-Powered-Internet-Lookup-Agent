# Use a lightweight Python image
FROM python:3.10-slim

# Create a non-root user for security
RUN useradd -m appuser

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app files
COPY . .

# Switch to non-root user
USER appuser

# Command to run your script
CMD ["python", "main.py"]
