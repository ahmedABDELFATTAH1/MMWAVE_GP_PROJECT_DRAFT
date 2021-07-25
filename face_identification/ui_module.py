from communication_Module import *
from logging import debug
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Output, Input ,State
# Create random data with numpy
import json 
import numpy as np
import plotly.express as px
import os, shutil
from communication_Module import _3D_mapping
import numpy as np
from plotly import offline
from plotly import graph_objs as go
from PIL import Image
import plotly.express as px
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from skimage.filters import threshold_minimum
import torch
import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from keras.models import load_model
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
np.random.seed(1)

def plot_hist(d,u,l):
    
    dist = d
    upper_angle = u
    lower_angle = l

    my_sample_y = np.array(dist)*np.cos(upper_angle)*np.cos(lower_angle)
    my_sample_y = my_sample_y[~np.isnan(my_sample_y)]

    # Set total number of bins in the histogram
    bins_num = [i for i in range(min_dist,max_dist,bin_size)]#256

    
    # Get the image histogram
    n = np.histogram(my_sample_y , bins = bins_num) 
    hist = n[0]
    bin_edges = n[1]
    # Calculate centers of bins
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.
    
    weight1 = np.cumsum(hist)
    
    weight2 = np.cumsum(hist[::-1])[::-1]
    
    # Get the class means mu0(t)
    mean1 = np.cumsum(hist * bin_mids) / weight1
    # Get the class means mu1(t)
    mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

    mean1 = np.nan_to_num(mean1)
    mean2 = np.nan_to_num(mean2)
    

    
    inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    # Maximize the inter_class_variance function val
    index_of_max_val = np.argmax(inter_class_variance)

    threshold = bin_mids[:-1][index_of_max_val]

    hist = [ hist[i] if bin_edges[i] < threshold else 0 for i in range(hist.size)]
    my_sample_y = my_sample_y[my_sample_y < threshold]
    
    total_value = np.sum(hist)
    hist_prob = hist / total_value
    hist_cumsum = np.cumsum(hist_prob)
    new_hist = hist_cumsum * 800
    new_hist = np.floor(new_hist).astype(int)
    new_my_sample_y = np.zeros(len(my_sample_y))
    for idx in range (len(my_sample_y)):
        for i in range(len(bin_edges)):
            if bin_edges[i]> my_sample_y[idx] :
                new_my_sample_y[idx] = new_hist[i-1]
                break

    
    n = np.histogram(new_my_sample_y , bins = bins_num) 
    hist_new = n[0]
    bin_edges_new = n[1]
    return threshold,hist,bin_edges,hist_new,bin_edges_new

def SVM_pred(d,u,l):
    model =load_model("SVM/partly_trained.h5")
    t , h, e , h_n , e_n = plot_hist(d,u,l)
    f = (h_n - np.min(h_n)) /(np.max(h_n) - np.min(h_n))
    data_list = np.array([f])
    y_pred = model.predict(data_list)
    return y_pred == 1

def points_to_image(d,u,l,threshold):
   
    dist = d
    upper_angle = u
    lower_angle = l

    my_sample_x = np.array(dist)*np.cos(upper_angle)*np.sin(lower_angle)
    my_sample_y =  np.array(dist)*np.cos(upper_angle)*np.cos(lower_angle)
    my_sample_z =  np.array(dist)*np.sin(upper_angle)
    
    my_sample_x = my_sample_x[~np.isnan(my_sample_x)]
    my_sample_y = my_sample_y[~np.isnan(my_sample_y)]
    my_sample_z = my_sample_z[~np.isnan(my_sample_z)]

    
    min_depth = np.amin(my_sample_y)
    max_depth = (min_depth + threshold)
    indx = my_sample_y <= (min_depth + threshold)

    my_sample_x = my_sample_x[indx]
    my_sample_y = my_sample_y[indx]
    my_sample_z = my_sample_z[indx]
    my_sample_y = 1-  (my_sample_y -  np.min(my_sample_y)) / (np.max(my_sample_y) - np.min(my_sample_y))
    x_min = np.min(my_sample_x)
    x_max = np.max(my_sample_x)
    y_min = np.min(my_sample_y)
    y_max = np.max(my_sample_y)
    z_min = np.min(my_sample_z)
    z_max = np.max(my_sample_z)
    width = 1+(x_max - x_min).astype(int)
    hight = 1+(z_max - z_min).astype(int)

    img = np.zeros((width,hight))
    
    for i in range(len(my_sample_x)):
        x = (my_sample_x[i] - x_min).astype(int)
        z = (my_sample_z[i] - z_min).astype(int)

        img[x,z] = my_sample_y[i]

    
    kernel = np.ones((5,5), np.uint8)

    img_dilation = cv2.dilate(img, kernel, iterations=3)

    dim = (64, 64)    
    resized = cv2.resize(img_dilation, dim, interpolation = cv2.INTER_AREA)
    
    return resized

def nn_pred(img):
    model =load_model("cnn/partly_trained.h5")
    img = np.reshape(img,(1,64,64, 1))
    result = model.predict(img)
    print("result :: ",result[0][0])
    return result[0][0] > 0.5 

def cnn_pred_one(d,u,l):
    t , h ,e , h_n, e_n= plot_hist(d,u,l)
    img = points_to_image(d,u,l,t)
    print("is this 3D object :: " ,nn_pred(img))

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
    'btncolor' : '#0170ad',
    'disabled_color' : '#AAAAAA',
    'footer_background' :'#6bc3e3'

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
    "position":"absolute"
}
app.layout = html.Div(children=[
    # html.Div(children='FACE RECOGNATION USING RADAR SYSTEM', style={
    #     'textAlign': 'center',
    #     'color': colors['text'],
    #     'marginTop':"10px",
    #     'fontSize':"40px"
    # }),
    html.Div(html.Img(style={"marginTop": "100px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 },
                          width="450px", height="450px", src="assets/gp_icon_with_logo.png"), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    }),
      html.Div(style={
        # "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"}, children=[ html.Button('Start Scan', id='start-scan', n_clicks=0 , style={
                  "width": "700px",
                   'height': "60px", 
                   "background": colors['btncolor'],
                   "color": colors['background'], 
                   'font-size' : '25px'}),
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
                          id = "original_hist" ,width="640px", height="480px", src ='',className='img'), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center"
    }),
    html.Div(html.Img(style={   "marginLeft": "20px",
                                 "alignSelf": "center",
                                 "margin": "auto",
                                 "display" : "none"
                                 },
                          id = "modified_hist",width="640px", height="480px", src ='',className='img'), style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center", 
    }), 
    html.H1(id = 'result_div' ,children='', style={
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center", 
        'color': colors['text'],
        # 'marginTop':"auto",
        "height":  "10rem",
        # 'marginBottom':"auto",
        'fontSize':"40px"
    }),  
    html.Div(id ="temp",children= 0 ,style={"display" : "none"}),
    html.Div( id = "footer_div",children ="© 2021 mmVision.  All rights reserved for Goodix Egypt.",style= {
        "justifyContent": "center",
        "justifyItems": "center",
        "textAlign": "center", 
        # "width": "100%",
        # "height" : "40px",
        "position":"fixed",
        # "buttom":'0',
        "background": colors['btncolor'],
        "color": colors['background'],
        'font-size' : '20px', 
        # "position": "fixed",
        "bottom": 0,
        "left": 0,
        "right": 0,
        "height":  "4rem",
        # 'marginTop':"auto"
        # "padding": "1rem 1rem",
        # "background-color": "gray",
    })
    

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
    return {"width": "700px",'height': "60px","background": colors['btncolor'],"color": colors['background'],'font-size' : '25px'} , 0



import random

min_dist = 0
max_dist=800
bin_size = 4
def plot_hist_dash(y):
    global min_dist,max_dist,bin_size
    
    n1 = random.randint(0,100)
    n2 = random.randint(0,100)
    my_sample_y = y
    my_sample_y = my_sample_y[~np.isnan(my_sample_y)]
    # Set total number of bins in the histogram
    bins_num = [i for i in range(min_dist,max_dist,bin_size)]#256
    # Get the image histogram

    
    # plt.figure(n1)
    
    n = plt.hist(my_sample_y , bins = bins_num, label='Original Histogram') 
    hist = n[0]
    bin_edges = n[1]
    # Calculate centers of bins
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.
    # Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # Get the class means mu0(t)
    mean1 = np.cumsum(hist * bin_mids) / weight1
    # Get the class means mu1(t)
    mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]
    mean1 = np.nan_to_num(mean1)
    mean2 = np.nan_to_num(mean2)
    inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2
    # Maximize the inter_class_variance function val
    index_of_max_val = np.argmax(inter_class_variance)
    threshold = bin_mids[:-1][index_of_max_val]
    print("Otsu's algorithm implementation thresholding result: ", threshold)
    
    plt.title("Original Histogram & Otsu's Threshold") 
    plt.xlabel("Horizontal Distances (mm)")
    plt.ylabel("Bin Value (bin size 4mm)")
    plt.axvline(threshold, color='r', label="Otsu's Threshold")
    plt.legend(loc='upper right')
    # plt.show()
    plt.savefig('assets/UI_folder/original_hist_'+str(n1)+'.png')
    # plt.close()
    # plt.figure(n2)
    plt.clf()

    plt.title("Foreground Histogram & Equalized Foreground Histogram") 
    plt.xlabel("Horizontal Distances (mm)")
    plt.ylabel("Bin Value (bin size 4mm)")
    hist = [ hist[i] if bin_edges[i] < threshold else 0 for i in range(hist.size)]
    my_sample_y = my_sample_y[my_sample_y <= threshold]
    
    total_value = np.sum(hist)
    hist_prob = hist / total_value
    hist_cumsum = np.cumsum(hist_prob)
    new_hist = hist_cumsum * 800
#     print ("hist_cumsum:: ",hist_cumsum)
    new_hist = np.floor(new_hist).astype(int)
#     print ("new_hist:: ",new_hist)
    new_my_sample_y = np.zeros(len(my_sample_y))
    for idx in range (len(my_sample_y)):
        for i in range(len(bin_edges)):
            if bin_edges[i]> my_sample_y[idx] :
#                 print("my_sample_y",my_sample_y[idx],"bin_edges",bin_edges[i],"i",i,"new_hist" ,new_hist[i-1])
                new_my_sample_y[idx] = new_hist[i-1]
                break


    plt.hist(my_sample_y, bins_num, alpha=0.8, label='Foreground Histogram')
    n = plt.hist(new_my_sample_y, bins_num, alpha=0.8, label='Equalized Foreground Histogram')
    hist_new = n[0]
    bin_edges_new = n[1]

    
    
    plt.legend(loc='upper right')
    plt.savefig('assets/UI_folder/modifidied_hist_'+str(n2)+'.png')
    # plt.close()
    plt.clf()
#     pyplot.show()
    
    
#     print("oh",hist)
#     print("nh",hist_n)
#     print("oy",bin_edges)
#     print("ny",new_my_sample_y)
    return threshold,hist,bin_edges,hist_new,bin_edges_new,n1,n2

@app.callback(Output('graph-3d-run', 'style'),
              Output('graph-3d-run', 'figure'),
              Output('original_hist', 'style'),
              Output('modified_hist', 'style'),
              Output('original_hist' , 'src'),
              Output('modified_hist' , 'src'),
              Output('result_div' , 'children'),
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

        fig = px.scatter_3d(df, x='X (mm)', y='Y (mm)', z='Z (mm)', color='Depth', range_color=[min_depth,max_depth],color_continuous_scale=color , opacity=1)  
        fig.update_layout(title_text="ٌ3d Mapping", title_x=0.5)          
        fig.update_traces(marker=dict(size=marker_size, line=dict(width=0))) 
        threshold,hist,bin_edges,hist_new,bin_edges_new,n1,n2 = plot_hist_dash(my_sample_y)

        pred = False
        result = "Result :: "
        #pred = SVM_pred(dist,uAngel,lAngel)
        #pred = cnn_pred_one(dist,uAngel,lAngel)
        if pred:
            result = result + "Face Detected"
        else:
            result = result + "Face Not Detected"

        return {'display': 'flex' , "marginBottom": "20px"} , fig , {'display': 'flex', "alignSelf": "center", "margin": "auto", "marginLeft": "20px",} ,{'display': 'flex', "alignSelf": "center", "margin": "auto", "marginLeft": "20px",} , '../assets/UI_folder/original_hist_'+str(n1)+'.png' , 'assets/UI_folder/modifidied_hist_'+str(n2)+'.png' , result

    
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
    
