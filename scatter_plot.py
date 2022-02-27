from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np


def scatter_plot(a, t, o):
    m_value = []  # create empty list to store calibration value
    b_value = []
    c_value = []
    d_value = []
    value = [m_value, b_value, c_value, d_value]

    m, b = np.polyfit(a, o, 1)  # find the slope and intercept of original data using numpy
    c, d = np.polyfit(t, o, 1)

    m_value.append(m)  # store the values  in empty list for further uses
    b_value.append(b)
    c_value.append(c)
    d_value.append(d)

    # plot monthly precipitation scatter plot from 2 data sources vs observed data
    plt.scatter(a, o, color='red', label='APHRODITE')
    plt.annotate("r-squared = {:.3f}".format(r2_score(o, a)), (0, 400), color='red')
    plt.plot(a, m * a + b, color='red', linestyle=':')

    plt.scatter(t, o, color='blue', label='TRMM')
    plt.annotate("r-squared = {:.3f}".format(r2_score(o, t)), (0, 350), color='blue')
    plt.plot(t, c * t + d, color='blue', linestyle=':')

    plt.title('Scatter Plot')
    plt.legend()
    plt.show()
    return value
