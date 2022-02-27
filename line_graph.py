import matplotlib.pyplot as plt


def line_graph(x, a, t, o, ty):

    plt.plot(x, a, label="APHRODITE_T", linestyle="-")  # plot monthly precipitation line graph from 3 data sources
    plt.plot(x, t, label="TRMM", linestyle="-.")
    plt.plot(x, o, label="Observed_T", linestyle=":")

    plt.title('{0}'.format(ty))
    plt.legend()
    plt.show()
