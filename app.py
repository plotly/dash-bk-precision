import argparse
import json
import copy
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

from dash.dependencies import Input, Output, State

from BKPDriver import SyncBKPDriver
from MockDriver import MockPSUDriver
from layout import dark_layout, light_layout, root_layout, external_css

driver = MockPSUDriver(0, 0.01)

app = dash.Dash("power_supply_appa", static_folder='')

if 'DYNO' in os.environ:
    if bool(os.getenv('DASH_PATH_ROUTING', 0)):
        app.config.requests_pathname_prefix = '/{}/'.format(
            os.environ['DASH_APP_NAME']
        )

app.layout = root_layout
app.scripts.config.serve_locally = True  # enables scripts to be sourced locally
app.config['supress_callback_exceptions'] = True
server = app.server
for css in external_css:
    app.css.append_css({"external_url": css})

default_layout = root_layout


@app.callback(Output('toggle-theme', 'value'), [Input('url', 'pathname')])
def update_theme(uri):
    if uri == '/dark':
        return True
    elif uri == '/light':
        return False


@app.callback(Output('content', 'children'), [Input('toggle-theme', 'value')])
def update_page(value):
    return dark_layout if value else light_layout


@app.callback(Output('content', 'style'), [Input('toggle-theme', 'value')])
def update_page(value):
    color = "white" if not value else "#506784"
    return {"background": color, "width": "100%", "height": "100%"}


@app.callback(
    Output('output-voltage', 'value'), [Input('store-data', 'children')])
def update_output_voltage(input):
    values = driver.read_supply_values()
    return "{:04.2f}".format(float(values["output_voltage"]))


@app.callback(
    Output('output-current', 'value'), [Input('store-data', 'children')])
def update_output_current(input):
    values = driver.read_supply_values()
    return "{:04.2f}".format(float(values["output_current"]))


@app.callback(
    Output('max-voltage', 'value'), [Input('store-data', 'children')])
def update_max_voltage(input):
    values = json.loads(input)
    return "{:04.2f}".format(float(values["maximum_voltage_setting"]))


@app.callback(
    Output('max-current', 'value'), [Input('store-data', 'children')])
def update_max_current(input):
    values = driver.read_supply_values()
    return "{:04.2f}".format(float(values["maximum_current_setting"]))


@app.callback(Output('submit', 'disabled'), [Input('status', 'value')])
def update_button(status):
    return not status


@app.callback(Output('status', 'value'), [Input('on-button', 'on')])
def on_power(input):
    values = driver.read_supply_values()
    driver.set_control(str(input))
    ret = driver.set_state(str(input))
    return input if ret else not input


@app.callback(
    Output('store-data', 'children'),
    [Input('output-update', 'n_intervals'),
     Input('status', 'value')])
def fetch_data(_1, _2):
    values = driver.read_supply_values()
    return json.dumps(values)


@app.callback(Output('submit', 'children'), [Input('choice', 'value')])
def on_choice_update(value):
    return "Set {}".format(value)


@app.callback(
    Output('error-label', 'children'), [Input('submit', 'n_clicks')],
    [State('set-value', 'value'),
     State('choice', 'value')])
def on_value_maybe_error(
        _,
        value,
        choice,
):
    try:
        value = float(value)
        if choice == "Voltage":
            driver.set_output_voltage(value)
        elif choice == "Max Current":
            driver.set_max_output_current(value)
        elif choice == "Max Voltage":
            driver.set_max_output_voltage(value)
    except ValueError as e:
        print(e)
        return "Error: {}".format(str(e))
    return ""


@app.callback(
    Output('error-label', 'hidden'), [Input('submit', 'n_clicks')],
    [State('set-value', 'value'),
     State('choice', 'value')])
def on_value_maybe_show_error(_, value, choice):
    try:
        value = float(value)
        if choice == "Voltage":
            driver.set_output_voltage(value)
        elif choice == "Max Current":
            driver.set_max_output_current(value)
        elif choice == "Max Voltage":
            driver.set_max_output_voltage(value)
    except ValueError as e:
        return False
    return True


@app.callback(
    Output('output-update', 'n_intervals'), [Input('submit', 'n_clicks')],
    [State('set-value', 'value'),
     State('choice', 'value')])
def on_value_update(
        _,
        value,
        choice,
):
    value = float(value)
    if choice == "Voltage":
        driver.set_output_voltage(value)
    elif choice == "Max Current":
        driver.set_max_output_current(value)
    elif choice == "Max Voltage":
        driver.set_max_output_voltage(value)

    return 0


if __name__ == '__main__':
    app.run_server(debug=False)
