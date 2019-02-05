import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import base64

logo_path = 'dash-daq-logo-by-plotly-stripe.png'
img = base64.b64encode(open(logo_path, 'rb').read())
light_header = html.Div(
    [
        html.H5(
            "BKPrecision Power Supply",
            style={
                'color': '#1d1d1d',
                'margin-left': '2%',
                'padding-top': '10px',
                'display': 'inline-block',
                'text-align': 'center'
            }),
        html.A(
            html.Img(
                src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                "excel/dash-daq/dash-daq-logo-by-plotly-stripe.png",
                style={
                    'position': 'relative',
                    'float': 'right',
                    'right': '10px',
                    'height': '75px'
                }),
            href='https://www.dashdaq.io')
    ],
    className='banner',
    style={
        'height': '75px',
        'margin': '0px -75px 10px',
        'background-color': '#F3F6A',
    })

dark_header = html.Div(children=[
    html.Div(
        [
            html.H5(
                "BKPrecision Power Supply",
                style={
                    'color': '#EBF0F8',
                    'margin-left': '2%',
                    'padding-top': '10px',
                    'display': 'inline-block',
                    'text-align': 'center'
                }),
            html.Img(
                src="https://s3-us-west-1.amazonaws.com/plotly-" +
                "tutorials/excel/dash-daq/dash-daq-logo-by-" +
                "plotly-stripe+copy.png",
                style={
                    'position': 'relative',
                    'float': 'right',
                    'right': '10px',
                    'height': '75px'
                })
        ],
        className='banner',
        style={
            'height': '75px',
            'margin': '0px -75px 10px',
            'background-color': 'black',
        })
])

light_top_box_style = {
    'width': '90%',
    'max-width': 'none',
    'font-size': '1.5rem',
    'background': '#F3F6FA',
    'color': '#2a3f5f',
    'border-radius': '5px 5px 0px 0px',
    'box-shadow': '0px 0px 0px 0px',
    'border': '1px solid #C8D4E3',
    'border-bottom': 'none'
}

light_bottom_box_style = {
    'width': '90%',
    'max-width': 'none',
    'font-size': '1.5rem',
    'color': 'black',
    'background': '#F3F6FA',
    'border-radius': '0px 0px 5px 5px',
    'box-shadow': '0px 0px 0px 0px',
    'border': '1px solid #C8D4E3'
}

dark_top_box_style = {
    'width': '90%',
    'max-width': 'none',
    'font-size': '1.5rem',
    'background': 'black',
    'color': 'white',
    'border-radius': '5px 5px 0px 0px',
    'box-shadow': '0px 0px 0px 0px'
}

dark_bottom_box_style = {
    'width': '90%',
    'max-width': 'none',
    'font-size': '1.5rem',
    'color': 'black',
    'background': '#F3F6FA',
    'border-radius': '0px 0px 5px 5px',
    'box-shadow': '0px 0px 0px 0px'
}

error_label_style = {
    "width": "400px",
    "margin": "20px auto",
    "padding": "10px",
    "color": "#EF553B",
    "text-align": "center",
    "background": "#DFEBF3",
    "border-radius": "2px",
    "border-left": "4px solid #EF553B"
}

top_box = html.Div([
    html.Div(
        className="row",
        children=[
            html.Label(children="Voltage", className="three columns"),
            html.Label(children="Current", className="three columns"),
            html.Label(children="Maximum Voltage", className="three columns"),
            html.Label(children="Maximum Current", className="three columns"),
        ],
    ),
    html.Div(
        className="row",
        children=[
            daq.LEDDisplay(
                id="output-voltage",
                className="three columns",
                color="#4ADE00",
            ),
            daq.LEDDisplay(
                id="output-current",
                className="three columns",
                color="#4ADE00"),
            daq.LEDDisplay(
                id="max-voltage", className="three columns", color="#4ADE00"),
            daq.LEDDisplay(
                id="max-current", className="three columns", color="#4ADE00")
        ]),
])

bottom_box = [
    html.Div(
        className="row",
        children=[
            daq.PowerButton(
                id="on-button",
                label="Power",
                on=False,
                className="one columns",
                color="#4AED00"),
            html.Div(
                className="two columns",
                children=[
                    html.Label(
                        children="Input",
                        className="row",
                        style={"padding": "0px 0px 10px 0px"}),
                    daq.NumericInput(
                        id='set-value',
                        value=0,
                        max=20,
                        size=120,
                        className="row",
                        style={"margin-bottom": "0"}),
                ]),
            html.Div(
                className="six columns",
                children=[
                    html.Label(
                        children="Input Type",
                        className="row",
                        style={"padding": "0px 0px 0px 0px"}),
                    dcc.RadioItems(
                        id='choice',
                        options=[{
                            "value": "Voltage",
                            "label": "Voltage"
                        }, {
                            "value": "Max Current",
                            "label": "Max Current"
                        }, {
                            "value": "Max Voltage",
                            "label": "Max Voltage"
                        }],
                        value="Voltage",
                        inputStyle={"padding": "0px 0px 0px 25px"},
                        labelStyle={"padding-top": "20px"},
                        inputClassName="three columns",
                        labelClassName="three columns",
                        className="row"),
                ]),
            html.Div(
                [
                    daq.StopButton(
                        id="submit",
                        size=150,
                    ),
                ],
                className="three columns",
                style={"padding-top": "25px"}),
        ]),
    html.Label(
        id='error-label',
        style=error_label_style,
        hidden=True,
    )
]

dark_top_box = html.Div(
    className="container",
    children=[dark_header] + [top_box],
    style=dark_top_box_style)
dark_bottom_box = html.Div(
    className="container", children=bottom_box, style=dark_bottom_box_style)

light_top_box = html.Div(
    className="container",
    children=[
        light_header,
        top_box
        ]
    )
light_bottom_box = html.Div(
    className="container", children=bottom_box
    )

dark_layout = html.Div(
    [daq.DarkThemeProvider(dark_top_box), dark_bottom_box],
    id='contentx',
    style={
        'color': '#2a3f5f',
        'padding': '50px 50px 50px 50px',
    })

light_layout = html.Div(
    [
        light_top_box,
        light_bottom_box,
    ],
    id='contentx',
    style={
        'color': '#F3F6FA',
        'padding': '50px 50px 50px 50px',
    })

root_layout = html.Div(
    [
        dcc.Interval(id='output-update', interval=3e6, n_intervals=0),
        html.Div([daq.Indicator(id='status', value=False)], hidden=True),
        html.Div(id="store-data", hidden=True),
        dcc.Location(id='url', refresh=False),
        html.Div(
            [
                daq.ToggleSwitch(
                    id='toggle-theme',
                    style={
                        'position': 'absolute',
                        'transform': 'translate(-50%, 20%)'
                    },
                    size=25),
            ],
            style={
                'width': 'fit-content',
                'margin': '0 auto'
            }),
        html.Div(
            id='content',
            children=light_layout,
            style={
                "background": "white",
                "width": "100%",
                "height": "100%",
                "margin": "0"
            }),
    ],
    style={"height": "100vh"})

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    "skeleton.css", "//fonts.googleapis.com/css?family=Raleway:400,300,600",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://codepen.io/chriddyp/pen/brPBPO.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"
]
