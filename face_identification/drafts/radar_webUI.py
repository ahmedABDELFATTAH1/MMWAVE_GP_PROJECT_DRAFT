# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd

# df = px.data.iris()

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Graph(id="scatter-plot"),
#     html.P("Petal Width:"),
#     dcc.RangeSlider(
#         id='range-slider',
#         min=0, max=2.5, step=0.1,
#         marks={0: '0', 2.5: '2.5'},
#         value=[0.5, 2]
#     ),
# ])

# @app.callback(
#     Output("scatter-plot", "figure"), 
#     [Input("range-slider", "value")])
# def update_bar_chart(slider_range):
#     low, high = slider_range
#     mask = (df.petal_width > low) & (df.petal_width < high)

#     fig = px.scatter_3d(df[mask], 
#         x='sepal_length', y='sepal_width', z='petal_width',
#         color="species", hover_data=['petal_width'])
#     return fig



# # Read data from a csv
# z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

# fig = go.Figure(data=[go.Surface(z=z_data.values)])
# fig.update_traces(contours_z=dict(show=True, usecolormap=True,
#                                   highlightcolor="limegreen", project_z=True))
# fig.update_layout(title='Mt Bruno Elevation', autosize=False,
#                   scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
#                   width=500, height=500,
#                   margin=dict(l=65, r=50, b=65, t=90)
# )



# fig.show()
# app.run_server(debug=True)
#################################################################################################################
##################################################################################################################
# import plotly.graph_objects as go
# import numpy as np
# import pandas as pd

# # Load data
# df = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
# df.columns = [col.replace("AAPL.", "") for col in df.columns]

# # Create figure
# fig = go.Figure()
# arr = [109,-18,-16,-30,	-11	,-20	,-46	,-47,	-50,	-54,	-55,	-58,	-65,	-73,	-65,	-63	,-76	,-72	,-75	,-73	,-74	,-72	,-76	,-77	,-76	,-82	,-79	,-76	,-82	,-83	,-83	,-83	,-89	,-90	,-93	,-86	,-92	,-84	,-87,	-86,	-86,	-89,	-90	,-118,-110,-120,-115,-111,-118,-113,-113,-116,-119,-119,-117,-109,-118,-117,-114,-121,-112,-115,-113,-113,-117,-131,-111,-123,-113,-111,-118,-121,-114,-122,-111,-119,-106,-115,-115,-125,-116,-115,-11,109,-18,-16,-30,	-11	,-20	,-46	,-47,	-50,	-54,	-55,	-58,	-65,	-73,	-65,	-63	,-76	,-72	,-75	,-73	,-74	,-72	,-76	,-77	,-76	,-82	,-79	,-76	,-82	,-83	,-83	,-83	,-89	,-90	,-93	,-86	,-92	,-84	,-87,	-86,	-86,	-89,	-90	,-118,-110,-120,-115,-111,-118,-113,-113,-116,-119,-119,-117,-109,-118,-117,-114,-121,-112,-115,-113,-113,-117,-131,-111,-123,-113,-111,-118,-121,-114,-122,-111,-119,-106,-115,-115,-125,-116,-115,-11]
# arr_x = np.arange(start=0, stop=1035, step=1)
# fig.add_trace(go.Scatter(x=arr_x, y=arr))

# # Set title
# fig.update_layout(
#     title_text="Time series with range slider and selectors"
# )

# # Add range slider
# fig.update_layout(
#     xaxis=dict(
#         rangeselector=dict(
            
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#         type="linear"
#     )
# )

# import json

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output

# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# app.run_server(debug=True)  # Turn off reloader if inside Jupyter
# # fig.show()
###############################################################################################################
################################################################################################################


# import dash 
# from dash.dependencies import Output, Input
# import dash_core_components as dcc 
# import dash_html_components as html 
# import plotly 
# import random 
# import numpy as np
# import plotly.graph_objs as go 
# from collections import deque 
# from radar_configuration import Radar
# from threading import Thread

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# global_distadnce = []
# # X = deque(maxlen = 20) 
# # X.append(1) 
  
# # Y = deque(maxlen = 20) 
# # Y.append(1) 
# radar = Radar()
# radar.setup_radar()
# def get_readings_thread():
#     global global_distadnce
#     while(True):
#         chance = radar.get_reading()
#         if (chance !=None):
#             global_distance = chance
#         print("global distance = ",global_distance)
# app = dash.Dash(__name__) 
  
# app.layout = html.Div(
# 	[
# 		html.H1('RADAR FACE IDENTIFICATION',style=external_stylesheets),
#         html.Div(id='live-update-text'),		 
# 		dcc.Graph(id='live-graph', animate=False),
# 		dcc.Interval(
# 			id='graph-update',
# 			interval=100,
# 			n_intervals=0
# 		),

# 	]
# )
  
# @app.callback( 
#     Output('live-graph', 'figure'), 
#     [ Input('graph-update', 'n_intervals') ] 
# ) 




# def update_graph_scatter(n): 
#     global X,Y,global_distadnce
#     Y = global_distadnce
#     print ("####################################################",Y)
#     # Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1)) 
  
#     data = plotly.graph_objs.Scatter( 
#             x=list(X), 
#             y=list(Y), 
#             name='Scatter', 
#             mode= 'lines+markers'
#     ) 
  
#     return {'data': [data], 
#             'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [-160,20]),)} 

# NUMBER_SAMPLES = 1024
# MAX_DISTANCE=1035
# X=[]
# Y=[]	
# def main():	
# 	global X
# 	X=np.linspace(0,MAX_DISTANCE,NUMBER_SAMPLES)	
# 	t1 = Thread(target = get_readings_thread,daemon=True) 
# 	t1.start()
# 	app.run_server()

# if __name__=='__main__':
# 	main()


###############################################################################################################
# from threading import Thread
# import numpy as np
# import matplotlib.pyplot as plt
# from radar_configuration import Radar
# import time
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# radar = Radar()
# radar.setup_radar()
# def get_readings_thread():
#     global last_reading
#     while(True):
#         print ("peak equal to = ",radar.get_median_distance(3))
#         chance = radar.get_reading()
#         if (chance !=None):
#             last_reading = chance
#         # print("global distance = ",last_reading)

# last_reading=None
# def main():	
# 	global last_reading
# 	t1 = Thread(target = get_readings_thread,daemon=True) 
# 	t1.start()
# 	x = list(range(0, 1024)) 
# 	y = list(np.zeros(1024))
# 	# print (y)
# 	plt.ion()

# 	figure, ax = plt.subplots()
# 	line1, = ax.plot(x, y)

# 	plt.title("Dynamic Plot of sinx",fontsize=25)

# 	plt.xlabel("X",fontsize=18)
# 	plt.ylabel("sinX",fontsize=18)
# 	figure.canvas.draw()
# 	while 1:
# 		updated_y = last_reading
# 		if updated_y == None:
# 			continue
# 		line1.set_xdata(x)
# 		line1.set_ydata(updated_y)
		
# 		figure.canvas.draw()
		
# 		figure.canvas.flush_events()
# 		time.sleep(0.1)

# 	# plt.ion()
# 	# fig = plt.figure()
# 	# ax = fig.add_subplot(111)
# 	# line1 = ax.plot(x, y, 'b-')
# 	# while 1:
# 	# # corresponding y axis values 
# 	# 	updated_y = last_reading
# 	# 	print (updated_y)
# 	# 	# plotting the points 
# 	# 	if updated_y == None:
# 	# 		continue
# 	# 	line1.set_xdata(x)
#     # 	line1.set_ydata(updated_y)
# 	# 	# line1 = ax.plot(x, y, 'b-')
# 	# 	fig.canvas.draw()
# 	# 	fig.canvas.flush_events()
# 	# 	time.sleep(0.1)
		

# if __name__=='__main__':
# 	main()
import time
from matplotlib import pyplot as plt
import numpy as np
from threading import Thread
from radar_configuration import Radar

radar = Radar()
radar.setup_radar()
def get_readings_thread():
    global global_distance
    while(True):
        chance = radar.get_reading()
        if (chance !=None):
            global_distance = chance
        # print("global distance = ",global_distance)

def live_update_demo(blit = False):
	global global_distance
	x = np.linspace(0,1024, 1024)
	# X,Y = np.meshgrid(x,x)
	fig = plt.figure()
	# ax1 = fig.add_subplot(2, 1, 1)
	ax2 = fig.add_subplot(1, 1, 1)

	# img = ax1.imshow(X, vmin=-1, vmax=1, interpolation="None", cmap="RdBu")


	line, = ax2.plot([], lw=3)
	text = ax2.text(0.8,0.5, "")

	ax2.set_xlim(x.min(), x.max())
	ax2.set_ylim([-160, 20])

	fig.canvas.draw()   # note that the first draw comes before setting data 


	if blit:
		# cache the background
		# axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
		ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

	plt.show(block=False)


	t_start = time.time()
	k=0.
	i = 2
	while 1:
		# img.set_data(np.sin(X/3.+k)*np.cos(Y/3.+k))
		line.set_data(x, global_distance)
		# tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) ) 
		# text.set_text(tx)
		#print tx
		k+=0.11
		if blit:
			# restore background
			# fig.canvas.restore_region(axbackground)
			fig.canvas.restore_region(ax2background)

			# redraw just the points
			# ax1.draw_artist(img)
			ax2.draw_artist(line)
			# ax2.draw_artist(text)

			# fill in the axes rectangle
			# fig.canvas.blit(ax1.bbox)
			fig.canvas.blit(ax2.bbox)

			# in this post http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
			# it is mentionned that blit causes strong memory leakage. 
			# however, I did not observe that.

		else:
			# redraw everything
			fig.canvas.draw()

		fig.canvas.flush_events()
		#alternatively you could use
		#plt.pause(0.000000000001) 
		# however plt.pause calls canvas.draw(), as can be read here:
		#http://bastibe.de/2013-05-30-speeding-up-matplotlib.html

global_distance = None
def main ():
	global global_distadnce
	t1 = Thread(target = get_readings_thread,daemon=False) 
	t1.start()

	while global_distance ==None:
		print (global_distance)
		pass
	live_update_demo(False)   # 175 fps
#live_update_demo(False) # 28 fps

if __name__  == "__main__":
	main()


######################################################################################################
# python_live_plot.py

# import random
# from itertools import count
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from radar_configuration import Radar
# from threading import Thread

# radar = Radar()
# radar.setup_radar()
# def get_readings_thread():
#     global global_distance
#     while(True):
#         chance = radar.get_reading()
#         if (chance !=None):
#             global_distance = chance
#         # print("global distance = ",global_distance)


# plt.style.use('fivethirtyeight')

# x_values = list(range(0, 1024))
# y_values = []

# index = count()


# def animate(i):
# 	global global_distance
# 	# x_values.append(next(index))
# 	y_values=global_distance

# 	plt.cla()
# 	plt.plot(x_values, y_values)

# global_distance = None
# t1 = Thread(target=get_readings_thread,daemon=True)
# t1.start()

# def main ():
# 	global global_distance
	
# 	ani = FuncAnimation(plt.gcf(), animate, 10000)
	
# 	plt.tight_layout()
# 	plt.show()

# if __name__ == "__main__":
# 	main ()
