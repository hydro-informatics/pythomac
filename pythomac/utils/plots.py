"""
Plot functions based on matplotlib
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_df(df, file_name, x_label=None, y_label=None, column_keyword="", legend=True):
    """ Plot a pandas DataFrame as lines with markers. The dataframe index is used for the x-axis.
    The function can handle a maximum of twelve columns

    :param pandas.DataFrame df: index serves for x-axis, columns containing a particular
        keyword are plotted on the y-axis (make sure these columns have the same units)
    :param str file_name: full path and name of the plot to be created
    :param str x_label: label for the x-axis
    :param str y_label: label for the y-axis
    :param str column_keyword: define a keyword that columns must contain to be plotted.
        The default '' (empty string) plots all columns.
    :param bool legend: place a legend (default is ``True``).
    :return:
    """

    font = {"size": 9}
    matplotlib.rc('font', **font)
    fig = plt.figure(figsize=(6, 3), dpi=400)
    axes = fig.add_subplot()
    colors = plt.cm.tab20(np.linspace(0, 1, len(df.columns)))  # https://matplotlib.org/stable/gallery/color/colormap_reference.html
    markers = ("x", "o", "s", "+", "1", "D", "*", "CARETDOWN", "3", "^", "p", "2")
    for i, y in enumerate(list(df)):
        if column_keyword in str(y).lower():
            axes.plot(
                df.index.values,
                df[y].abs(),
                color=colors[i],
                markersize=2,
                marker=markers[i],
                markerfacecolor="none",
                markeredgecolor=colors[i],
                linestyle="-",
                linewidth=1.0,
                alpha=0.6,
                label=y
            )
    axes.set_xlim((np.nanmin(df.index.values), np.nanmax(df.index.values)))
    axes.set_ylim(bottom=0)
    if x_label:
        axes.set_xlabel(x_label)
    if y_label:
        axes.set_ylabel(y_label)
    if legend:
        axes.legend(loc="best", facecolor="white", edgecolor="gray", framealpha=0.5)
    fig.tight_layout()
    fig.savefig(file_name)
    print("* saved plot: " + str(file_name))
