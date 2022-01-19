# Dash celery mwe

This repository holds a minimal working example of how a (long) job can be run asynchronously in Plotly Dash using Celery and Azure infrastructure. 

## Running the example

Create a virtual environment and install the requirements,

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Copy the .env.example file to a .env file and in values in brackets [] (can be found in the [Azure portal](https://portal.azure.com/)). Next, start the worker process,

    celery -A cl.tasks worker --pool solo 

Finally, spin up the app process,

    python app.py

You should now be able to view the app on `localhost:8050`.