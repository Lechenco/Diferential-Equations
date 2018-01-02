#Vamos salvar a Apollo 13
#radius_of_earth = 6.371e6 #m

#import math
#import numpy


###############
# QUIZ
# 
# Fill in the for loop below to set 
# the x, y1, and y2 arrays to the 
# following values:
#
# - The x array should contain 
#   num_points many points evenly 
#   spaced between 0 and 2*pi.
#   0 and 2*pi should be included.
#
# - The y1 array should contain 
#   the corresponding sine values 
#   of the values in the x array.
#
# - The y2 array should contain 
#   the corresponding cosine values
#   of the values in the x array.

import math
import matplotlib.pyplot
import numpy
#from udacityplots import *


def sin_cos():
    num_points = 50

    sin_x = numpy.zeros(num_points)
    x = numpy.zeros(num_points)
    cos_x = numpy.zeros(num_points)

    for step in range(num_points):
        x[step] = 2 * math.pi * step / (num_points - 1)
        sin_x[step] = math.sin(x[step])
        cos_x[step] = math.cos(x[step])

    return x, sin_x, cos_x

x, sin_x, cos_x = sin_cos()

# These lines call the matplotlib package
# to plot the values you input on a graph.

def plot_me():
    matplotlib.pyplot.plot(x, sin_x)
    matplotlib.pyplot.plot(x, cos_x)
plot_me()
