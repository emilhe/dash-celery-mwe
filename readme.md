# Dash celery mwe

This repository holds a minimal working example of how a (long) job can be run asynchronously in Plotly Dash using Celery and Redis. 

## Running the example

Create a virtual environment and install the requirements,

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Make sure that Redis is available on `localhost:6379`. It can be spun up e.g. using docker,

    sudo docker run --name my-first-redis -d redis

Next, start the worker process,

    celery -A cl.tasks worker --loglevel=info

Finally, spin up the app process,

    python app.py

You should now be able to view the app on `localhost:8050`.