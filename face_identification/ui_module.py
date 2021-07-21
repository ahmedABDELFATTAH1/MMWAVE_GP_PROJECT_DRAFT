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

folder_name = "UI_folder/"
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
        "textAlign": "center"}, children=[ html.Button('Start Scan', id='start-scan', n_clicks=0),
        ]),       
        dcc.Graph(id="graph-3d-run",figure=fig3d,style={
            'height':'700px',
            "display" : "none"
        }),
        html.Div(html.Img(style={"marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 "display" : "none"
                                 },
                          id = "original_hist" ,width="80px", height="80px", src="assets/company_logo.png"), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    }),
    html.Div(html.Img(style={"marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 "display" : "none"
                                 },
                          id = "modified_hist",width="80px", height="80px", src="assets/company_logo.png"), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    })

], style=body)



scanning = False
scanning_count = -1
Done_scanning = False

# @app.callback([Output('start-scan','style'),Output('save-scan','style')],
#     [Input('start-scan', 'n_clicks')]
#     ,[State('start-scan', 'style'),State('file_name_id', 'value')])
# def start_scan_event(n_clicks,button_style,file_name):  
#     print(file_name)  
#     global scanning , scanning_count
#     if scanning:        
#         return red_button_style,disabled_button_style
#     else:
#         if scanning_count < 0 :
#             scanning_count +=1
#             return white_button_style,disabled_button_style
#         if file_name is None or file_name == "" or file_name.replace(" ", "")==0:
#             return white_button_style,disabled_button_style
#         if len(file_name.split(' '))> 1:
#             return white_button_style,disabled_button_style
#         scanning = True    
#         Scan3d(file_name)
#         scanning = False
#         return white_button_style,white_button_style

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

@app.callback(Output('graph-3d-run', 'style'),
              Output('graph-3d-run', 'figure'),
              Output('original_hist', 'style'),
              Output('modified_hist', 'style'),
              [Input('start-scan', 'n_clicks')])
def update_output(n_clicks):
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

        return {'display': 'block'} , fig , {'display': 'block'} ,{'display': 'block'} 

   

        # list_of_names = ["waleed_14_7_100_x.txt","waleed_14_7_100_y.txt","waleed_14_7_100_z.txt"]
        # for file_name in list_of_names:
        #     print(len(file_name))
        #     numbers = np.loadtxt("3D_Experements/"+file_name)            
        #     #print(numbers[0:100])
        #     if(file_name.split('.')[0][-1].lower()=='x'):
        #         dist = numbers
        #     elif(file_name.split('.')[0][-1].lower()=='y'):
        #         upper_angle = numbers
        #     elif(file_name.split('.')[0][-1].lower()=='z'):
        #         lower_angle = numbers
        # if(dist is None or upper_angle is None or lower_angle is None):
        #     return {'display': 'block'} , fig3d , {'display': 'block'} ,{'display': 'block'}
        # else:   
        #     my_sample_x = np.array(dist)*np.cos(upper_angle)*np.sin(lower_angle)*-1
        #     my_sample_y = np.array(dist)*np.cos(upper_angle)*np.cos(lower_angle)
        #     my_sample_z = np.array(dist)*np.sin(upper_angle)*-1

        #     # my_sample_x,my_sample_y,my_sample_z = filter_points(my_sample_x,my_sample_y,my_sample_z)

        #     df = pd.DataFrame(my_sample_x,columns=['X (mm)'])
        #     df['Y (mm)'] = my_sample_y
        #     df['Z (mm)'] = my_sample_z
            
        #     min_depth = 0
        #     max_depth = 0

        #     df['Depth'] = my_sample_y
        #     max_depth = np.amax(my_sample_y)
        #     min_depth = np.amin(my_sample_y)

          
        #     fig = px.scatter_3d(df, x='X (mm)', y='Y (mm)', z='Z (mm)', color='Depth', title="ٌ3d Mapping" , range_color=[min_depth,max_depth],color_continuous_scale=color , opacity=1)
        #     fig.update_traces(marker=dict(size=marker_size, line=dict(width=0)))             

        #     return {'display': 'block'} , fig3d , {'display': 'block'} ,{'display': 'block'} 

    
    return {'display': 'none'} , fig3d , {'display': 'none'} , {'display': 'none'}
show_figures = False

# def get_reading_message(): 
#     context = zmq.Context()
#     consumer_receiver = context.socket(zmq.SUB)
#     consumer_receiver.RCVTIMEO = 1000
#     consumer_receiver.setsockopt_string(zmq.SUBSCRIBE, "")    
#     consumer_receiver.connect("tcp://127.0.0.1:5558")
#     frame = None
#     try:
#         frame = consumer_receiver.recv_json()   
#     except:
#         pass
#     # print(frame)
#     consumer_receiver.close() 
#     return frame 




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
    df = px.data.tips()
    print (df.head()) 
    setup()
    app.run_server()
    
