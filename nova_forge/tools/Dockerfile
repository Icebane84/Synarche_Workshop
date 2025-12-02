# 1. THE BASE (The Foundation)
# We start with a lightweight version of Linux that has Python pre-installed.
FROM python:3.9-slim

# 2. THE WORKSPACE (The Kitchen)
# Create a directory inside the container to hold your code.
WORKDIR /app

# 3. THE DEPENDENCIES (The Ingredients)
# Copy the requirements file first to leverage Docker's "Layer Caching".
COPY requirements.txt .
# Install libraries (e.g., Flask, NumPy).
RUN pip install --no-cache-dir -r requirements.txt

# 4. THE CODE (The Meal)
# Copy the rest of your source code into the container.
COPY . .

# 5. THE COMMAND (The Serving Suggestion)
# Tell the container what command to run when it starts up.
CMD ["python", "app.py"]

