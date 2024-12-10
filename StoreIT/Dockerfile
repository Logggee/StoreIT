# Dockerfile

# pull offical python base image
FROM python:3.12.7-slim

# set the working sirectory in for the application insight the container
# The directory gets created if it does not exist
WORKDIR /app/StoreIT

# Set enviroment variables for the container
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install all application dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the complete project into the working directory
COPY . .

# Collect all static files and put them under STATIC_ROOT
RUN python manage.py collectstatic --noinput