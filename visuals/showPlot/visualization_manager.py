import matplotlib as mpl
mpl.use('WebAgg')
import matplotlib.pyplot as plt
import numpy as np

#This code will create a scatter plot

# pass array in this format  [(1, 7), (2, 8), (3, 9), (4, 8)]
def generate_scattered_graph(node_array, xaxis_name, yaxis_name):
    x = [p[0] for p in node_array]
    y = [p[1] for p in node_array]

    area = np.pi * 1.5

    # Plot
    plt.scatter(x, y, s=area)
    plt.xlabel(xaxis_name)
    plt.ylabel(yaxis_name)
    plt.show()


#arr = [(1, 7), (2, 8), (3, 9), (4, 8)]
#generate_scattered_graph(node_array=arr, xaxis_name="x axis", yaxis_name="y axis")
