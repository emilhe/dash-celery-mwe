FROM python:3.8-slim-buster

# Create a working directory.
RUN mkdir wd
WORKDIR wd

# Install Python dependencies.
COPY ./cl/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY ./cl/tasks.py ./cl/tasks.py

# Finally, run celery.
CMD [ "celery", "-A", "cl.tasks", "worker", "--loglevel=info"]
