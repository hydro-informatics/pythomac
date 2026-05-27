"""
Plot functions based on matplotlib
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def plot_df(df, file_name, x_label=None, y_label=None, column_keyword="", legend=True, tight_ylim=False, hline=None):
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
    :param float hline: if set, draw a dashed horizontal reference line at this y-value
        (excluded from the legend). The y-limits are widened to keep the line visible.
    :return:
    """

    font = {"size": 9}
    matplotlib.rc('font', **font)
    fig = plt.figure(figsize=(6, 3), dpi=400)
    axes = fig.add_subplot()
    colors = plt.cm.cool(np.linspace(0, 1, len(df.columns)))  # https://matplotlib.org/stable/gallery/color/colormap_reference.html
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
        # widen the band so the reference line stays inside the plotted area
        if hline is not None:
            y_min, y_max = min(y_min, hline), max(y_max, hline)
        # snap limits to multiples of a nice tick step so gridlines (incl. the
        # bottom axis and top box line) are evenly spaced
        tick_values = mticker.MaxNLocator(nbins=6).tick_values(y_min, y_max)
        tick_step = tick_values[1] - tick_values[0]
        lower = np.floor(y_min / tick_step) * tick_step
        upper = np.ceil(y_max / tick_step) * tick_step
        if upper <= lower:
            upper = lower + tick_step
        axes.yaxis.set_major_locator(mticker.MultipleLocator(tick_step))
        axes.set_ylim(lower, upper)
        if hline is not None:
            # force a labeled tick at the reference value (only for this plot)
            ticks = np.arange(lower, upper + tick_step / 2, tick_step)
            ticks = np.unique(np.append(ticks, hline))
            axes.yaxis.set_major_locator(mticker.FixedLocator(ticks))
    else:
        axes.set_ylim(bottom=0)
    if hline is not None:
        axes.axhline(y=hline, color="black", linestyle="--", linewidth=0.8, label="_nolegend_")
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
