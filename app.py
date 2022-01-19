
from flask import Flask
from cl.tasks import take_a_nap, celery_app
from celery.result import result_from_tuple
from dash_extensions.enrich import DashProxy, MultiplexerTransform, Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate

# Create app.
server = Flask(__name__)
app = DashProxy(server=server, transforms=[MultiplexerTransform()], prevent_initial_callbacks=True)
app.layout = html.Div([
    # User input (how many second to nap).
    dcc.Input(id="nap-duration", type="number", min=0, max=10, value=1),
    # Button for launching async job (a nap).
    html.Button(id="btn-run", children="Take a nap"),
    # Container for storing the result of the async job.
    html.Div(id="div-result"),
    # Container for storing a reference to the async job.
    dcc.Store(id="result-tuple"),
    # Interval component for polling updates on the status of the async job.
    dcc.Interval(id="poller", max_intervals=0),
])


@app.callback([Output("btn-run", "disabled"), Output("btn-run", "children"),
               Output("result-tuple", "data"), Output("poller", "max_intervals")],
              [Input("btn-run", "n_clicks")], [State("nap-duration", "value")])
def launch_job(n_clicks, value):
    # Run the job asynchronously (note the .delay syntax).
    result = take_a_nap.delay(str(value))
    # Disable button and set text (or start a spinner, etc.), save result reference, and start polling.
    return True, "Napping...", result.as_tuple(), -1


@app.callback([Output("btn-run", "disabled"), Output("btn-run", "children"),
               Output("div-result", "children"), Output("poller", "max_intervals")],
              [Input("poller", "n_intervals")], [State("result-tuple", "data")])
def poll_result(n_intervals, data):
    if not data:
        raise PreventUpdate()
    result = result_from_tuple(data, app=celery_app)
    # If the calculation has not completed, do nothing.
    if not result.ready():
        raise PreventUpdate()
    # On completion, enable button and set text (or stop spinner, etc.), return the result, and stop polling.
    return False, "Take a nap", str(result.get()), 0


if __name__ == '__main__':
    app.run_server()
