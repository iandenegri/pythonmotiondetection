import pandas
from motiondetect import df
from bokeh.plotting import figure, show,output_file
from bokeh.models import HoverTool, ColumnDataSource

# convert datatime to string types
df['Start_string']=df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['End_string']=df['End'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Data conversion for presenting in the tooltip.
cds=ColumnDataSource(df)

p=figure(height=100,width=500,x_axis_type='datetime',responsive=True,title='Motion Detection Graph')
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[('Start',"@Start_string"),('End', '@End_string')])
p.add_tools(hover)

q=p.quad(left='Start',right='End',bottom=0,top=1,color='blue', source=cds)

output_file=('movement_times.html')

show(p)
