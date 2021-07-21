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
from arduino_configuration import Arduino
import plotly.express as px
import base64
import io
import os, shutil
from communication_Module import _3D_mapping
np.random.seed(1)



global_reading =np.random.uniform(low=0.5, high=13.3, size=(50,))
global_index = 1
configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
# port = configuration_json["PORT"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


color = px.colors.sequential.Rainbow[::-1]
marker_size = 5

dist = np.loadtxt("3D_Experements/"+"waleed_14_7_100_x.txt") 
upper_angle = np.loadtxt("3D_Experements/"+"waleed_14_7_100_y.txt") 
lower_angle = np.loadtxt("3D_Experements/"+"waleed_14_7_100_z.txt") 

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


fig3d = px.scatter_3d(df, x='X (mm)', y='Y (mm)', z='Z (mm)', color='Depth', title="ٌRadar Point Cloud:" , range_color=[min_depth,max_depth],color_continuous_scale=color , opacity=1)
fig3d.update_traces(marker=dict(size=marker_size, line=dict(width=0)))             

folder_name = "assets/UI_folder/"
scan_name = "temp"


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
        # "float": "right"
    }, children=[html.Div(html.Img(style={#"marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 },
                          width="250px", height="250px", src="assets/gp_icon.png"), style={
        # "justifyContent": "center",
        # "justifyItems": "center",
        "textAlign": "center"
    }),html.H1(children='SPONSERED BY GOODIX EGYPT', style={
        'fontSize': "20px",
        'fontWeight':'bold',
        'color': colors['mytext'],
        "alignSelf": "center",
        "margin": "auto",
        "textAlign": "center"
    }), html.Div(html.Img(style={"marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 },
                          width="80px", height="80px", src=app.get_asset_url("company_logo.png")), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    })]),
    
    #    dcc.Interval(
    #     id='graph-update',
    #     interval=500,
    #     n_intervals=0,
    #     disabled=False
    # )   ,
   
      html.Div(style={
        # "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"}, children=[ html.Button('Start Scan', id='start-scan', n_clicks=0 ),
        ]),       
        dcc.Graph(id="graph-3d-run",figure=fig3d,style={
            'height':'700px',
            "display" : "none"
        }),
        html.Div(html.Img(style={
                                 
                                 "display" : "none",
                                 "marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto"
                                 },
                          id = "original_hist" ,width="640px", height="480px", src = "UI_folder/original_hist.png"), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    }),
    html.Div(html.Img(style={   "marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 "display" : "none"
                                 },
                          id = "modified_hist",width="640px", height="480px",src = "UI_folder/original_hist.png"), style={
       "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    }), 
    html.Div(id ="temp",children= 0 ,style={"display" : "none"}), 

], style=body)



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



@app.callback(
              Output('start-scan' , 'style'),
              Output('temp' , 'children'),
              [Input('start-scan', 'n_clicks')])
def update_output_1(n_clicks):
    if n_clicks > 0 :
        return {'display': 'none'} , 1


@app.callback(Output('graph-3d-run', 'style'),
              Output('graph-3d-run', 'figure'),
              Output('original_hist', 'style'),
              Output('modified_hist', 'style'),
              Output('original_hist' , 'src'),
              Output('modified_hist' , 'src'),
              [Input('temp', 'children')])
def update_output(n_clicks):
    clear_ui_folder()
    dist = None
    upper_angle = None
    lower_angle = None

    print("im  working :::" , n_clicks)
    
    if  n_clicks != 0:
        dist,uAngel,lAngel = _3D_mapping(scan_name+"_"+str(n_clicks),folder_name)
        x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
        my_sample_x = np.array(x)
        my_sample_y = np.array(y)
        my_sample_z = np.array(z)

        df = pd.DataFrame()
    
        indx = []
        min_depth = 0
        max_depth = 0
        

        
           
           
    
        df['Depth'] = my_sample_y


        df['X (mm)'] = my_sample_x
        df['Y (mm)'] = my_sample_y
        df['Z (mm)'] = my_sample_z
        # df.head()

        fig = px.scatter_3d(df, x='X (mm)', y='Y (mm)', z='Z (mm)', color='Depth', title="ٌ3d Mapping" , range_color=[min_depth,max_depth],color_continuous_scale=color , opacity=1)
        fig.update_traces(marker=dict(size=marker_size, line=dict(width=0)))             

        plot_hist(my_sample_y)

        return {'display': 'flex'} , fig , {'display': 'flex'} ,{'display': 'flex'} , 'assets/UI_folder/original_hist.png' , 'assets/UI_folder/modifidied_hist.png'

    
    return {'display': 'none'} , fig3d , {'display': 'none'} , {'display': 'none'}
show_figures = False

    
def clear_ui_folder():
    folder = 'assets/UI_folder'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    
if __name__ == '__main__': 
    setup()
    app.run_server()
    
