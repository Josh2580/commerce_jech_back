# Dockerfile for Django
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port 8000 for Django
EXPOSE 8000


# Set the default environment variable (or load it later)
ENV SECRET_KEY=${SECRET_KEY}


# # Copy entrypoint.sh into the container and make it executable
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# # Run entrypoint.sh as the entry point for this container
# ENTRYPOINT ["/entrypoint.sh"]

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
