# Use an official Python runtime as a parent image
FROM python:3.9.1

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV DEBUG=True
ENV SECRET_KEY='django-insecure-a7n@3hu_tdhh%i8!#w7v&dq_enrih06qoa4+^l=nn)q8$@tpqw'

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run Django's development server with the .env file
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
