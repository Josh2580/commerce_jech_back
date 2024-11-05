# Dockerfile for Django
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .



# Making migrate
RUN python manage.py migrate

# Expose the port 8000 for Django
EXPOSE 8000

# Start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Run migrations, collect static files, and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]





