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
		# html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
		# html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
		# html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
    	# html.Div(id='container-button-timestamp'),
        # html.Div(id='live-update-text'),		 
		dcc.Graph(id='live-graph', animate=False),
		dcc.Interval(
			id='graph-update',
			interval=100,
			n_intervals=0
		),
		
	]
)


# @app.callback(Output('container-button-timestamp', 'children'),
#               Input('btn-nclicks-1', 'n_clicks'),
#               Input('btn-nclicks-2', 'n_clicks'),
#               Input('btn-nclicks-3', 'n_clicks'))
			  
# def displayClick(btn1, btn2, btn3):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'btn-nclicks-1' in changed_id:
#         msg = 'Button 1 was most recently clicked'
#     elif 'btn-nclicks-2' in changed_id:
#         msg = 'Button 2 was most recently clicked'
#     elif 'btn-nclicks-3' in changed_id:
#         msg = 'Button 3 was most recently clicked'
#     else:
#         msg = 'None of the buttons have been clicked yet'
#     return html.Div(msg)


# @app.callback(Output('live-update-text', 'children'),
#               Input('graph-update', 'n_intervals'))
# def update_metrics(n):
# 	style = {'padding':'5px','fontsize':'16px'}
# 	threashold=-20
# 	Y=None
# 	if last_reading is not None:
# 		Y=last_reading
# 	else:
# 		return[
# 		html.Span("Hello",style=style)
# 	]

# 	distance, magnitude = naive_face_detection(Y)
# 	if(magnitude is None):
# 		return[
# 		html.Span("Hello",style=style)
# 	]
# 	text = ""
# 	if magnitude < threashold:
# 		text = 'there is no face sorry'
# 	else:
# 		text = 'there is a face at distance ' + str(distance)
	
# 	return[
# 		html.Span(text,style=style)
# 	]
    

@app.callback( 
	Output('live-graph', 'figure'), 
	[ Input('graph-update', 'n_intervals') ] 
) 
def update_graph_scatter(n): 
	global X,Y,last_reading
	print(last_reading)
	if last_reading is not None:
		Y=last_reading
	Y=[-136, -123, -112, -105, -99, -95, -92, -89, -87, -85, -84, -83, -82, -81, -80, -80, -80, -80, -80, -80, -80, -81, -82, -82, -83, -84, -85, -86, -87, -88, -89, -90, -91, -92, -93, -93, -94, -94, -94, -94, -94, -94, -94, -94, -95, -95, -96, -96, -97, -98, -99, -100, -102, -103, -104, -106, -108, -110, -111, -113, -114, -115, -114, -113, -111, -109, -107, -104, -102, -100, -99, -97, -96, -94, -93, -92, -91, -91, -90, -90, -89, -89, -89, -89, -90, -90, -91, -92, -93, -94, -96, -97, -100, -103, -106, -111, -115, -112, -108, -104, -99, -95, -92, -89, -86, -84, -82, -80, -79, -78, -77, -76, -75, -75, -75, -75, -75, -76, -77, -79, -81, -84, -89, -95, -103, -104, -95, -87, -80, -75, -71, -67, -64, -61, -59, -57, -56, -54, -53, -53, -52, -52, -52, -53, -54, -55, -57, -60, -63, -68, -75, -80, -77, -69, -62, -56, -51, -48, -45, -42, -40, -38, -37, -36, -35, -35, -35, -35, -36, -37, -39, -41, -44, -48, -54, -60, -61, -54, -46, -40, -35, -31, -28, -25, -23, -21, -20, -18, -18, -17, -17, -17, -18, -19, -20, -22, -25, -30, -36, -44, -47, -38, -28, -21, -15, -11, -7, -4, -1, 1, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, 15, 15, 16, 16, 16, 16, 15, 15, 15, 14, 13, 12, 11, 10, 9, 7, 5, 3, 1, -1, -4, -8, -12, -17, -23, -31, -37, -35, -30, -25, -21, -18, -15, -14, -12, -12, -11, -11, -11, -12, -12, -13, -14, -16, -17, -19, -22, -24, -28, -31, -35, -40, -45, -50, -51, -50, -47, -44, -41, -39, -38, -37, -37, -37, -37, -38, -39, -41, -42, -45, -47, -51, -55, -60, -65, -70, -70, -67, -63, -59, -56, -53, -51, -50, -49, -48, -48, -48, -48, -49, -50, -50, -52, -53, -55, -57, -59, -62, -65, -68, -71, -75, -78, -82, -85, -86, -89, -84, -79, -76, 
-74, -73, -71, -71, -70, -70, -70, -70, -70, -71, -71, -72, -73, -74, -74, -75, -76, -77, -78, -78, -78, -77, -77, -76, -76, -75, -74, -73, -73, -72, -72, -71, -71, -71, -71, -71, -71, -71, -71, -71, -71, -71, -72, -73, -73, -74, -76, -77, -78, -79, -79, -80, -80, -79, -79, -78, -77, -76, -75, -73, -72, -70, -69, -68, -66, -65, -64, -62, -61, -61, -60, -59, -59, -58, -58, -58, -59, -59, -60, -61, -62, -63, -65, -66, -69, -72, -74, -70, -66, -62, -58, -54, -51, -48, -46, -44, -42, -40, -38, -37, -35, -34, -33, -32, -31, -31, -30, -30, -30, -30, -30, -30, -30, -31, -31, -32, -33, -34, -35, -37, -38, -40, -42, -44, -47, -49, 
-51, -53, -54, -53, -52, -51, -49, -47, -46, -45, -44, -43, -42, -42, -41, -41, -42, -42, -43, -43, -44, -45, -47, -48, -50, -52, -54, -57, -60, -64, -68, -73, -77, -79, -79, -76, -73, -69, -67, -64, -63, -62, -61, -60, -60, -60, -60, -61, -61, -62, -63, -64, -65, -67, -68, -69, -71, -72, -74, -76, -77, -79, -80, -81, -82, -82, -82, -83, -83, -85, -86, -89, -93, -95, -91, -90, -89, -88, -88, -88, -88, -86, -85, -85, -84, -83, -82, -82, -81, -80, -80, -80, -79, -79, -80, -80, -80, -80, -81, -81, -82, -84, -83, -82, -82, -82, -82, -83, -83, -84, -84, -85, -86, -87, -88, -90, -90, -90, -89, -89, -89, -89, -88, -87, -87, -86, 
-86, -85, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -74, -73, -73, -72, -72, -72, -71, -71, -71, -71, -72, -72, -72, -72, -72, -73, -73, -74, -75, -76, -77, -78, -80, -82, -84, -85, -84, -84, -85, -85, -86, -87, -88, -89, -90, -90, -91, -92, -91, -91, -91, -91, -90, -90, -91, -91, -91, -92, -92, -92, -93, -93, -93, -94, -94, -94, -95, -95, -95, -95, -95, -95, -95, -95, -95, -95, -94, -93, -93, -92, -91, -91, -91, -90, -90, -90, -90, -90, -90, -90, -90, -90, -90, -90, -90, -90, -90, -90, -91, -91, -92, -93, -95, -96, -97, -98, -99, -101, -104, -106, -105, -104, -102, -101, -100, -99, -98, -97, -97, -96, -96, -95, -95, -95, -94, -94, -94, -94, -95, -95, -96, -97, -98, -99, -100, -101, -103, -105, -108, -110, -106, -104, -103, -101, -101, -100, -100, -99, -98, -98, -98, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -98, -99, -99, -100, -100, -100, -101, -101, -102, -102, -102, -102, -103, -103, -104, -104, -105, -106, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -108, -108, -109, -110, -109, -109, -108, -108, -109, -108, -108, -108, -109, -109, -109, -109, -109, -109, -109, -109, -109, -109, -109, -109, -109, -109, -110, -110, -110, -111, -111, -111, -112, -112, -113, -114, -115, -116, -118, -119, -120, -122, -124, -126, -128, -130, -131, -131, -132, -133, -134, -136, -137, -139, -142, -141, -140, -139, -138, -136, -134, -132, -130, -129, -128, -127, -126, -125, -125, -125, -124, -124, -124, -124, -124, -124, -125, -125, -126, -125, -126, -126, -126, -126, -127, -127, -127, -127, -128, -128, -128, -128, -129, -129, -129, -130, -130, -131, -132, -132, -133, -134, -134, -135, -136, -138, -139, -142, -146, -145, -143, -142, -142, -142, -142, -142, -142, -142, -142, -142, -142, -142, -142, -142, -142, -142, -143, -143, -143, -144, -144, -145, -145, -146, -147, -148, -149, -149, -150, -151, -153, -155, -156, -154, -153, -151, -151, -150, -150, -150, -150, -150, -151, -151, -151, -151, -151, -151, -152, -152, -151, -151, -150, -150, -150, -150, -151, -151, -151, -151, -152, -152, -153, -154, -155, -156, -158, -160, -163, -165, -166, -165, -165, -165, -165, -166, -166, -167, -169, -170, -171, -173, -174, -176, -177, -178, -178, -178, -178, -178, -178, -178, -177, -177, -176, -176, -175, -174, -173, -173, -173, -172, -172, -171, -171, -170, -170, -169, -169, -168, -167, -167, -166, -166, -165, -164, -164, -163, -162, -162, -161, -161, -160, -160, -160, -159, -159, -159, -159, -159, -159, -159, -159, -159, -159, -159]
	data = plotly.graph_objs.Scatter( 
		 	x=list(X),
			y=list(Y), 
			name='Scatter', 
			mode= 'lines+markers'
	) 

	return {'data': [data], 
			'layout' :go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [-160,20]))			
			} 

NUMBER_SAMPLES = 1024
last_reading=None
MAX_DISTANCE=2048
X=[]
Y=[]	
def main():	
	global X
	X=np.linspace(0,MAX_DISTANCE,NUMBER_SAMPLES)	
	# t1 = Thread(target = get_readings,daemon=True) 
	# t1.start()
	app.run_server()


if __name__=='__main__':
	main()
	
