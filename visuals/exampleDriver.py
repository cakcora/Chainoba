
#The generate_scattered_graph() and generate_box_plot() functions are imported from the visualization_manager.py file
from visuals.visualization_manager import generate_scattered_graph, generate_box_plot

#Total nine points will be displayed in scatter graph. Each point consists of x and y coordinates. These are passed in an array.
arr = [(2,5), (1, 7), (2, 8), (3, 9), (4, 8),(6,9),(4,8),(1,6),(5,11)]
#The scatter graph will be generated.
generate_scattered_graph(node_array=arr, xaxis_name="x axis", yaxis_name="y axis")

#y1, y2 and y3 are the three boxes that will be displayed in box plot.
#The three integer values inside the variables specifies the size of the boxes.
#The minimum value and maximum value specifies the range.
# And the remaining value is the median of the box.
y1 = (4, 2, 3)
y2 = (4, 3, 1)
y3 = (3, 1, 2)

#The variables for boxes generation are passed in array.
arr = [y1, y2, y3]

#The box plot is generated.
generate_box_plot(node_array=arr, xaxis_name="x axis", yaxis_name="y axis")

