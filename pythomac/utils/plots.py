"""
Plot functions based on matplotlib
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_df(df, file_name, x_label=None, y_label=None, column_keyword="", legend=True, tight_ylim=False):
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
    :param bool tight_ylim: if True, set the y-limits to narrowly embrace the plotted data
        (with a small margin) instead of anchoring the bottom at zero. Useful when values
        cluster in a narrow band (e.g., convergence rates around 1.0).
    :return:
    """

    font = {"size": 9}
    matplotlib.rc('font', **font)
    fig = plt.figure(figsize=(6, 3), dpi=400)
    axes = fig.add_subplot()
    colors = plt.cm.tab20(np.linspace(0, 1, len(df.columns)))  # https://matplotlib.org/stable/gallery/color/colormap_reference.html
    markers = ("x", "o", "s", "+", "1", "D", "*", "CARETDOWN", "3", "^", "p", "2")
    plotted_values = []
    for i, y in enumerate(list(df)):
        if column_keyword in str(y).lower():
            y_values = df[y].abs()
            plotted_values.append(np.asarray(y_values, dtype=float))
            axes.plot(
                df.index.values,
                y_values,
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
    if tight_ylim and plotted_values:
        all_values = np.concatenate(plotted_values)
        all_values = all_values[np.isfinite(all_values)]
        y_min, y_max = np.nanmin(all_values), np.nanmax(all_values)
        span = y_max - y_min
        margin = 0.1 * span if span > 0 else max(abs(y_max), 1.0) * 1e-6
        axes.set_ylim(y_min - margin, y_max + margin)
    else:
        axes.set_ylim(bottom=0)
    axes.tick_params(axis="both", direction="in")
    if x_label:
        axes.set_xlabel(x_label)
    if y_label:
        axes.set_ylabel(y_label)
    if legend:
        axes.legend(loc="best", facecolor="white", edgecolor="gray", framealpha=0.5)
    axes.grid(color="gray", linestyle='-', linewidth=0.5)
    fig.tight_layout()
    fig.savefig(file_name)
    print("* saved plot: " + str(file_name))
