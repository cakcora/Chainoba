#This code has two functions, generate_scattered_graph() and generate_box_plot().
#These functions are called from the exampleDriver.py


import matplotlib as mpl
#'WebAgg' is required to show the plots in web interface
mpl.use('WebAgg')
import matplotlib.pyplot as plt
import numpy as np

#This function takes an array of nodes and names for x axis and y axis.
def generate_scattered_graph(node_array, xaxis_name, yaxis_name):

    # Variable x takes all the coordinates of x from node_array using for loop.
    x = [p[0] for p in node_array]
    # Variable y takes all the coordinates of y from node_array using for loop.
    y = [p[1] for p in node_array]
    # The variable area specifies the total area the plot will be displayed in
    area = np.pi * 2.5

    # Generating a scatter plot by using the x and y arrays and area.
    plt.scatter(x, y, s=area)
    # The labels of the plots are specified
    plt.xlabel(xaxis_name)
    plt.ylabel(yaxis_name)
    #Scatter plot will be showed in the browser instance, as 'WebAgg' is used.
    plt.show()

#This function takes an array of nodes and names of a axis and y axis.
def generate_box_plot(node_array, xaxis_name="x axis", yaxis_name="y axis"):

    #This line specifies the range of axises.

    #Variables a1,b1 and c1 takes three boxes to be plotted in the box plot
    a1 = node_array[0]
    b1 = node_array[1]
    c1 = node_array[2]

    # Variables max1 and min1 defines the x and y ranges of the box plot.
    # 2 is added with the maximum value and -2 is added with minimum value to make the boxes and the graph nice.
    max1 = max(max(a1), max(b1), max(c1)) + 2
    min1 = min(min(a1), min(b1), min(c1)) - 2

    plt.axis([min1, max1, min1, max1])

    #Plots the boxplot consisting of three boxes
    plt.boxplot([a1, b1, c1])
    #The labels of the plot are specified
    plt.xlabel(xaxis_name)
    plt.ylabel(yaxis_name)

    plt.show()



