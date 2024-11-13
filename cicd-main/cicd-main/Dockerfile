# Use a base image with Python
FROM python:3.7.2-stretch

# Set the working directory
WORKDIR /app

# Install Flask and any other required packages
#RUN pip install Flask  # You can add other dependencies here

# Copy the entire application code and test script into the container
COPY . /app

# Copy the requirements file if you have one
# Uncomment and create requirements.txt if needed
# COPY requirements.txt .
RUN pip install -r configure.txt

# Expose the port the app runs on
EXPOSE 8888

# Command to run the Flask app
CMD ["python", "main.py"]  # Replace app.py with the name of your main application file