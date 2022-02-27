from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
from scatter_plot import scatter_plot
from line_graph import line_graph


def calibration(a, t, o):
    ty = 'Calibrated Line Graph'
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']  # x-axis of line graph

    a_c = []  # create empty list to store calibrated data
    t_c = []

    value = scatter_plot(a, t, o)  # get calibration coefficient from scatter_plot function

    a_c.append(a * value[0] + value[1])  # store the calibrated value into empty list
    t_c.append(t * value[2] + value[3])

    m, b = np.polyfit(o, a_c[0], 1)  # find the slope and intercept of calibrated data using numpy
    c, d = np.polyfit(o, t_c[0], 1)

    line_graph(x, a_c[0], t_c[0], o, ty)  # plot calibrated monthly precipitation line graph from 3 data sources

    # plot calibrated monthly precipitation scatter plot from 2 data sources vs observed data
    plt.scatter(o, a_c, color='red', label='APHRODITE')
    plt.annotate("r-squared = {:.3f}".format(r2_score(o, a_c[0])), (0, 400), color='red')
    plt.plot(o, (m * o + b), color='red', linestyle=':')

    plt.scatter(o, t_c, color='blue', label='TRMM')
    plt.annotate("r-squared = {:.3f}".format(r2_score(o, t_c[0])), (0, 350), color='blue')
    plt.plot(o, (c * o + d), color='blue', linestyle=':')

    plt.title('Calibrated Scatter Plot'.format('year'))
    plt.legend()
    plt.show()
