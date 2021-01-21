from threading import Thread
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import numpy as np
import plotly
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import object_detection
from radar_configuration import Radar


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def get_readings():
	global last_reading
	'''
	this function will be an opned thread to take readings from the radar
	it will get frames from the radar then produce it in the queue
	'''
	radar = Radar(port='com5')
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
		html.H1('RADAR FACE IDENTIFICATION',style=external_stylesheets),		
		html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
		html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
		html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
    	html.Div(id='container-button-timestamp'),
        html.Div(id='live-update-text'),		 
		dcc.Graph(id='live-graph', animate=False),
		dcc.Interval(
			id='graph-update',
			interval=100,
			n_intervals=0
		),
		
	]
)


@app.callback(Output('container-button-timestamp', 'children'),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('btn-nclicks-2', 'n_clicks'),
              Input('btn-nclicks-3', 'n_clicks'))
			  
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        msg = 'Button 1 was most recently clicked'
    elif 'btn-nclicks-2' in changed_id:
        msg = 'Button 2 was most recently clicked'
    elif 'btn-nclicks-3' in changed_id:
        msg = 'Button 3 was most recently clicked'
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div(msg)


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

NUMBER_SAMPLES = 255
last_reading=None
MAX_DISTANCE=8268.8
X=[]
Y=[]	
def main():	
	global X
	X=np.linspace(0,MAX_DISTANCE,NUMBER_SAMPLES)	
	t1 = Thread(target = get_readings,daemon=True) 
	t1.start()
	app.run_server()


if __name__=='__main__':
	main()
	