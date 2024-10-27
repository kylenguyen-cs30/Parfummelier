
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the service will run on
EXPOSE 5004

# Run the command to start the Flask app
# CMD ["flask", "run", "--host=1.0.0.0"]
# CMD ["flask", "run"]
CMD ["flask", "run", "--host=0.0.0.0"]

