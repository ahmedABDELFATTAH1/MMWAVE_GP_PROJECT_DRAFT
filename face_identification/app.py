import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly
from dash.dependencies import Output, Input
# Create random data with numpy
import numpy as np
np.random.seed(1)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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

    return px.scatter(df, x="x", y="y", color="color")


# fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
fig = update_2d_graph(np.random.uniform(low=0.5, high=13.3, size=(50,)), 1, 1)
fig.data[0].update(mode='markers')


colors = {
    'background': '#111111',
    'text': '#e3f2fd',
    'mytext': '#e3f2fd'
}

markdown_text = '''
# Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

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
        interval=100,
        n_intervals=100
    ),
    html.Div(style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"}, children=[html.Button('Start Scan', id='submit-val', n_clicks=0, style={
            "backgroundColor": colors['mytext']
        }), html.Button('Start Scan', id='submit-vall', n_clicks=0, style={
            "backgroundColor": colors['mytext']
        })])


], style=body)


@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    fig = update_2d_graph(np.random.uniform(low=0.5, high=13.3, size=(50,)), 1, 1)
    fig.data[0].update(mode='lines+markers')
    fig.update_layout(uirevision="foo")
    #draw.data[0].update(mode='lines+markers')
    #fig.add_trace(draw)
    #fig.update_layout(uirevision="foo")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
