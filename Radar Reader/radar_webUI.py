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
def get_readings(q):
	radar=Radar(port='com4')
	if(radar.is_open()):
		radar.close()
	radar.start()
	count=1
	while 1:
		reading=radar.read_magnitude()
		count+=1		
		if reading is not None:
			if q.full():
				q.queue.clear()
			q.put(reading)



	

app = dash.Dash(__name__) 

app.layout = html.Div( 
	[ 
		dcc.Graph(id = 'live-graph', animate = True), 
		dcc.Interval( 
			id = 'graph-update', 
			interval = 100, 
			n_intervals = 0
		), 
	] 
) 

@app.callback( 
	Output('live-graph', 'figure'), 
	[ Input('graph-update', 'n_intervals') ] 
) 


def update_graph_scatter(n): 
	global X,Y,q	
	if not q.empty():
		Y_new=q.get()
		print('hellooo')	
		print(len(Y_new))	
		if(len(Y_new)==255):	
			print(Y_new[0])		
			Y=Y_new	
			print(len(Y))
			print(len(X))
		else:			
			Y=np.zeros(len(X))	
	print('yessssss')
	data = plotly.graph_objs.Scatter( 
			x=list(X), 
			y=list(Y), 
			name='Scatter', 
			mode= 'lines+markers'
	) 

	return {'data': [data], 
			'layout' :go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [-140,0]),)			
			} 


from queue import Queue 
from threading import Thread



if __name__=='__main__':
	X=[]
	X=np.linspace(0,8268.8,255)
	Y=[]
	q = Queue(50)	
	t1 = Thread(target = get_readings, args =(q, )) 
	t1.start()
	app.run_server()
	