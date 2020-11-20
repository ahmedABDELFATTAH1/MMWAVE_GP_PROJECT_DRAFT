import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from radar_configuration import Radar
import numpy as np
import time
from radar_signal_processeing import naive_face_detection
from queue import Queue 
from threading import Thread
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def get_readings():
	global last_reading
	'''
	this function will be an opned thread to take readings from the radar
	it will get frames from the radar then produce it in the queue
	'''
	radar = Radar(port='com4')
	if(radar.is_open()):
		radar.close()
	radar.start()	
	radar.clear_buffer()
	while 1:
		reading = radar.read_magnitude()		
		if reading is not None:
			last_reading=reading


app = dash.Dash(__name__)

app.layout = html.Div(
	[
		html.H4('RADAR FACE IDENTIFICATION'),
        html.Div(id='live-update-text'),
		dcc.Graph(id='live-graph', animate=False),
		dcc.Interval(
			id='graph-update',
			interval=100,
			n_intervals=0
		),
	]
)


@app.callback(Output('live-update-text', 'children'),
              Input('graph-update', 'n_intervals'))
def update_metrics(n):
	style = {'padding':'5px','fontsize':'16px'}
	threashold=-20
	Y=None
	if last_reading is not None:
		Y=last_reading
	else:
		return[
		html.Span("Hello",style=style)
	]

	distance, magnitude = naive_face_detection(Y)
	if(magnitude is None):
		return[
		html.Span("Hello",style=style)
	]
	text = ""
	if magnitude < threashold:
		text = 'there is no face sorry'
	else:
		text = 'there is a face at distance ' + str(distance)
	
	return[
		html.Span(text,style=style)
	]
    

@app.callback( 
	Output('live-graph', 'figure'), 
	[ Input('graph-update', 'n_intervals') ] 
) 
def update_graph_scatter(n): 
	global X,Y,last_reading
	print(last_reading)
	if last_reading is not None:
		Y=last_reading
	data = plotly.graph_objs.Scatter( 
			x=list(X), 
			y=list(Y), 
			name='Scatter', 
			mode= 'lines+markers'
	) 

	return {'data': [data], 
			'layout' :go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [-160,20]))			
			} 




if __name__=='__main__':
	X=[]
	X=np.linspace(0,8268.8,255)
	Y=[]	
	last_reading=None
	t1 = Thread(target = get_readings,daemon=True) 
	t1.start()
	app.run_server()
