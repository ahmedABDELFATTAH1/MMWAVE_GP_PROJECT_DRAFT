from typing import Mapping
from communication_Module import *
from logging import debug
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly
from dash.dependencies import Output, Input ,State
# Create random data with numpy
import json 
import sys
import zmq
import pickle
import numpy as np
from threading import Thread
from radar_configuration import Radar
import plotly.express as px
import base64
import io
np.random.seed(1)



global_reading =np.random.uniform(low=0.5, high=13.3, size=(50,))
global_index = 1
configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
port = configuration_json["PORT"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def update_2d_graph(y, index, bin_resolution):
    x = [i for i in range(0, len(y))]
    color = ['green' if i != index else "red" for i in x]
    df = pd.DataFrame({
        "Frame FFT()": np.array(x)*bin_resolution,
        "Magnitude(dB)": y,
        "color": color
    })

    return px.scatter(df, x="Frame FFT()", y="Magnitude(dB)", color="color")

# fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
fig = update_2d_graph(np.random.uniform(low=0.5, high=13.3, size=(50,)), 1, 1)
fig.data[0].update(mode='markers')
#fig = update_2d_graph(global_reading, global_index, 1)


color = px.colors.sequential.Rainbow[::-1]
marker_size = 5




dist = np.loadtxt("3D_Experements/"+"face3_x.txt") 
upper_angle = np.loadtxt("3D_Experements/"+"face3_y.txt") 
lower_angle = np.loadtxt("3D_Experements/"+"face3_z.txt") 

my_sample_x = np.array(dist)*np.cos(upper_angle)*np.sin(lower_angle)
my_sample_y = np.array(dist)*np.cos(upper_angle)*np.cos(lower_angle)
my_sample_z = np.array(dist)*np.sin(upper_angle)

df = pd.DataFrame(my_sample_x,columns=['X (mm)'])
df['Y (mm)'] = my_sample_y
df['Z (mm)'] = my_sample_z

min_depth = 0
max_depth = 0

df['Depth'] = my_sample_y
max_depth = np.amax(my_sample_y)
min_depth = np.amin(my_sample_y)


fig3d = px.scatter_3d(df, x='X (mm)', y='Y (mm)', z='Z (mm)', color='Depth', title="ٌRadar Point Cloud" , range_color=[min_depth,max_depth],color_continuous_scale=color , opacity=1)
fig3d.update_traces(marker=dict(size=marker_size, line=dict(width=0)))             





colors = {
    'background': '#FFFFFF',
    'text': '#111111',
    'mytext': '#111111',
    'btncolor' : '#6495ED',
    'disabled_color' : '#AAAAAA'
}


white_button_style = {
            "backgroundColor": colors['btncolor'],
            "color": colors['background'],
            "marginLeft" : "30px"
        }

disabled_button_style = {
            "backgroundColor": colors['disabled_color'],
            "color": colors['text'],
            "marginLeft" : "30px"
        }

red_button_style = {'background-color': 'red',
                    'color': 'white',
                   }


body = {
    'backgroundColor': colors['background'],
    "width": "100%",
    "height": "100%",
    "position": "absolute"
}
app.layout = html.Div(children=[
    html.Div(children='FACE RECOGNATION USING RADAR SYSTEM', style={
        'textAlign': 'center',
        'color': colors['text'],
        'marginTop':"10px",
        'fontSize':"40px"
    }),
    html.Div(style={
        "float": "right"
    }, children=[html.Div(html.Img(style={"marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 },
                          width="125px", height="250px", src=app.get_asset_url("gp_logo.png"), alt="Girl in a jacket"), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    }),html.H1(children='SPONSERED BY GOODIX EGYPT', style={
        'fontSize': "20px",
        'fontWeight':'bold',
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
    
      html.Div(children = [ html.Div(style={
        "justifyContent": "center",
        "justifyItems": "center",
         "margin-top": "50px",
        "textAlign": "center"},children = [html.Button('Show Readings', n_clicks=0, id='frame_visualise_button',style={        
        "margin":"auto",        
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"})])
        ,dcc.Graph(id='live-graph', figure=fig, style={       
        "width": "70%",
       
     })
      ]),  
       dcc.Interval(
        id='graph-update',
        interval=500,
        n_intervals=0,
        disabled=False
    )   ,
   
      html.Div(style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"}, children=[ dcc.Input(
            id="file_name_id",
            type="text",
            placeholder="enter file name",
        ),html.Button('Start Scan', id='start-scan', n_clicks=0, style=white_button_style),
        html.Button('Save Scan', id='save-scan', n_clicks=0, style=disabled_button_style)]),       
        dcc.Graph(id="graph-3d-run",figure=fig3d,style={
            'height':'1000px'
        }),    
         dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Graph(id="graph-3d-save",figure=fig3d,style={
        'width':"100%",
        'height':'1000px'
    })

], style=body)



scanning = False
scanning_count = -1
Done_scanning = False

@app.callback([Output('start-scan','style'),Output('save-scan','style')],
    [Input('start-scan', 'n_clicks')]
    ,[State('start-scan', 'style'),State('file_name_id', 'value')])
def start_scan_event(n_clicks,button_style,file_name):  
    print(file_name)  
    global scanning , scanning_count
    if scanning:        
        return red_button_style,disabled_button_style
    else:
        if scanning_count < 0 :
            scanning_count +=1
            return white_button_style,disabled_button_style
        if file_name is None or file_name == "" or file_name.replace(" ", "")==0:
            return white_button_style,disabled_button_style
        if len(file_name.split(' '))> 1:
            return white_button_style,disabled_button_style
        scanning = True    
        Scan3d(file_name)
        scanning = False
        return white_button_style,white_button_style

def filter_points(x,y,z):
    new_samples_x = []
    new_samples_y = []
    new_samples_z = []
    for x,y,z in zip(x,y,z):
        if y < 510:
            new_samples_x.append(x)
            new_samples_y.append(y)
            new_samples_z.append(z)
    return np.array(new_samples_x),np.array(new_samples_y),np.array(new_samples_z)

@app.callback(Output('graph-3d-save', 'figure'),
              [Input('upload-data', 'contents'),
              Input('upload-data', 'filename'),
              Input('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    dist = None
    upper_angle = None
    lower_angle = None
    if list_of_contents is not None:
        for file_name in list_of_names:
            print(len(file_name))
            numbers = np.loadtxt("3D_Experements/"+file_name)            
            #print(numbers[0:100])
            if(file_name.split('.')[0][-1].lower()=='x'):
                dist = numbers
            elif(file_name.split('.')[0][-1].lower()=='y'):
                upper_angle = numbers
            elif(file_name.split('.')[0][-1].lower()=='z'):
                lower_angle = numbers
        if(dist is None or upper_angle is None or lower_angle is None):
            return fig3d
        else:   
            my_sample_x = np.array(dist)*np.cos(upper_angle)*np.sin(lower_angle)*-1
            my_sample_y = np.array(dist)*np.cos(upper_angle)*np.cos(lower_angle)
            my_sample_z = np.array(dist)*np.sin(upper_angle)*-1

            # my_sample_x,my_sample_y,my_sample_z = filter_points(my_sample_x,my_sample_y,my_sample_z)

            df = pd.DataFrame(my_sample_x,columns=['X (mm)'])
            df['Y (mm)'] = my_sample_y
            df['Z (mm)'] = my_sample_z
            
            min_depth = 0
            max_depth = 0

            df['Depth'] = my_sample_y
            max_depth = np.amax(my_sample_y)
            min_depth = np.amin(my_sample_y)

          
            fig = px.scatter_3d(df, x='X (mm)', y='Y (mm)', z='Z (mm)', color='Depth', title="ٌ3d Mapping" , range_color=[min_depth,max_depth],color_continuous_scale=color , opacity=1)
            fig.update_traces(marker=dict(size=marker_size, line=dict(width=0)))             

            return fig
    return fig3d
show_figures = False

def get_reading_message(): 
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.SUB)
    consumer_receiver.RCVTIMEO = 1000
    consumer_receiver.setsockopt_string(zmq.SUBSCRIBE, "")    
    consumer_receiver.connect("tcp://127.0.0.1:5558")
    frame = None
    try:
        frame = consumer_receiver.recv_json()   
    except:
        pass
    # print(frame)
    consumer_receiver.close() 
    return frame 




@app.callback(
    [dash.dependencies.Output('frame_visualise_button', 'children'),dash.dependencies.Output('frame_visualise_button', 'style'),
    dash.dependencies.Output('graph-update','disabled')],
    [dash.dependencies.Input('frame_visualise_button', 'n_clicks')])
def update_output1(n_clicks): 
    print("hello")   
    global show_figures
    print(n_clicks)
    if n_clicks%2 ==0:  
        show_figures = False
        return "Show Readings",white_button_style , True
    else:
        show_figures = True
        return "Stop Readings",red_button_style , False
   
    




@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    [Input('graph-update', 'n_intervals')],
    [State('live-graph', 'figure')]
)
def update_graph_scatter(n,figure):
    print("hello12")
    if not show_figures:
        return figure
    frame = np.random.uniform(low=0.5, high=13.3, size=(50,))    
    frame = get_reading_message()
    if frame is None:
        return figure
    # print(frame)
    frame = frame["FRAME"]  
    index, distance, db_frame = radar.detect_peaks(frame, True, None)
    print("index value = "+str(index))
    fig = update_2d_graph(frame, index, 2.1)
    fig.data[0].update(mode='lines+markers')
    fig.update_layout(uirevision="foo")
    return fig




    
if __name__ == '__main__':    
    app.run_server()
    
