import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly
from dash.dependencies import Output, Input
# Create random data with numpy
import json 
import numpy as np
from threading import Thread
from radar_configuration import Radar
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

global_frame = -1

def get_readings_thread():
    global global_frame
    radar = Radar()
    radar.setup_radar()
    while(1):
        frame = radar.get_reading()
        # frame = np.random.uniform(low=0.5, high=13.3, size=(50,))
        print(len(frame))
        global_frame = frame


# configuration_file = open('configuration.json',)
# configuration_json = json.load(configuration_file)
# bin_resolution = configuration_json["BIN_RESOLUTION"] 

# np.random.seed(1)

# global_reading =np.random.uniform(low=0.5, high=13.3, size=(50,))
# radar =Radar()


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
'''
N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

fig = go.Figure()

fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                    mode='lines+markers',
                    name='lines+markers'))
'''


def update_2d_graph(y, index, bin_resolution):
    x = [i for i in range(0, len(y), bin_resolution)]
    color = ['green' if i != index else "red" for i in x]
    df = pd.DataFrame({
        "x": x,
        "y": y,
        "color": color
    })

    return px.scatter(df, x="x", y="y", color="color", range_y = [-140,30])


# fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
# fig = update_2d_graph(np.random.uniform(low=0.5, high=13.3, size=(50,)), 1, 1)
#fig = update_2d_graph(global_reading, 1, bin_resolution)
#fig.data[0].update(mode='markers')


colors = {
    'background': '#FFFFFF',
    'text': '#111111',
    'mytext': '#111111',
    'btncolor' : '#6495ED'
}


body = {
    'backgroundColor': colors['background'],
    "width": "100%",
    "height": "100%",
    "position": "absolute"
}

app.layout = html.Div(children=[
    html.Div(children='FACE IDENTIFICATION USING RADAR SYSTEM', style={
        'textAlign': 'center',
        'color': colors['text'],
        'marginTop':"10px",
        'fontSize':"40px"
    }),
    html.Div(style={
        "float": "right"
    }, children=[html.H1(children='SPONSERED BY GOODIX EGYPT', style={
        'fontSize': "20px",
        'color': colors['mytext'],
        'marginRight':"50px"

    }), html.Div(html.Img(style={"marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 },
                          width="80px", height="80px", src=app.get_asset_url("company_logo.png"), alt="Girl in a jacket"), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    })]),

    dcc.Graph(id='live-graph', figure=fig, style={
        "position": "relative",
        "width": "70%",
        "margin": "50px"
    }),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=1
    ),
    html.Div(style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"}, children=[html.Button('Start Scan', id='submit-val', n_clicks=0, style={
            "backgroundColor": colors['btncolor'],
            "color": colors['background']
        }), html.Button('Start Scan', id='submit-vall', n_clicks=0, style={
            "backgroundColor": colors['btncolor'],
            "color": colors['background']
        })])


], style=body)


@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    index,_ = radar.detect_peaks(frame)
    fig = update_2d_graph(frame, index, bin_resolution)
    fig.data[0].update(mode='lines+markers')
    fig.update_layout(uirevision="foo")
    return fig
    
if __name__ == '__main__':
    t1 = Thread(target=get_readings_thread,daemon=True)
    t1.start()
    t1.join()
    app.run_server(debug=True)
    
