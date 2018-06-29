import datetime as datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import colorConverter
import seaborn as sns


def prepare_plot():
    """
    Set up general plot aesthetics to be used for including figures in a manuscript or talk.
    These defaults are possibly too large for interactive use.
    This function should be called before `paper_plot`.
    """
    sns.set()
    # Increase font size and linewidth
    sns.set_context("notebook", font_scale=2, rc={"lines.linewidth": 5})
    sns.set_style("white")
    # Use LaTeX, setup to use Helvetica. This can be safely commented to make
    # the installation footprint of running this code smaller -- for example,
    # in Docker.
    mpl.rc("text", usetex=True)
    mpl.rcParams["text.latex.preamble"] = [
        r"\usepackage{amsmath}",
        r"\usepackage{helvet}",
        r"\usepackage[EULERGREEK]{sansmath}",
        r"\sansmath",
        r"\renewcommand{\familydefault}{\sfdefault}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{graphicx}",
    ]


def paper_plot(
    fig,
    adjustment=0,
    scientific=False,
    save=False,
    filename=None,
    raster=False,
    label_pad=True,
):
    """
    Take a prepared figure and make additional adjustments for inclusion in manuscript:
    mostly tick thickness, length, and label padding, and include only the left and the bottom
    axis spines. It would be nice to force the axes to end on a major tick, but I haven't
    figured out how to do that yet.
    """
    for ax in fig.axes:
        # Increase padding
        ax.tick_params(which="major", direction="out", length=10, pad=10)
        ax.tick_params(which="minor", direction="out", length=5)
        # If plotting with pi, increase the x tick size specifically
        # ax.tick_params(axis='x', labelsize=40, pad=-10)
        # Increase tick thickness
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if label_pad:
            # Increase padding
            ax.xaxis.labelpad = 15
            ax.yaxis.labelpad = 15
        # Make the background color white
        facecolor = "white"
        if facecolor is False:
            facecolor = fig.get_facecolor()
        alpha = 1
        color_with_alpha = colorConverter.to_rgba(facecolor, alpha)
        fig.patch.set_facecolor(color_with_alpha)
        # Stick the scientific notation into the axis label, instead of the
        # default position which in the corner, which really makes no sense.
        if ax.xaxis.get_scale() == "linear":
            if scientific:
                pretty_label(ax)
            ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
            ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        elif ax.xaxis.get_scale() == "log":
            pass
        # For scatter plots, where points get cut off
        if adjustment != 0:
            x0, x1, y0, y1 = ax.axis()
            ax.xaxis((x0 - adjustment, x1 + adjustment, y0, y1))
        # Make axes thicker
        for axis in ["top", "bottom", "left", "right"]:
            ax.spines[axis].set_linewidth(2)
    if save:
        plt.savefig(filename + ".png", dpi=300, bbox_inches="tight")
        plt.savefig(filename + ".svg", dpi=300, bbox_inches="tight")


def setup_plot(y_label, x_label, axis_padding=0.06):
    """
    Another helper function that can be used to create time-stampped plots.
    """
    # https://stackoverflow.com/questions/31928209/matplotlib-fixed-spacing-between-left-edge-of-figure-and-y-axis
    fig_width = 6 * 1.2
    fig_height = 6
    fig = plt.figure(figsize=(fig_width, fig_height))
    left_margin = 0.95 / fig_width
    right_margin = 0.20 / fig_width
    bottom_margin = 0.50 / fig_height
    top_margin = 0.25 / fig_height
    x = left_margin + axis_padding  # horizontal position of bottom-left corner
    y = bottom_margin  # vertical position of bottom-left corner
    w = 1 - (left_margin + right_margin)  # width of axes
    h = 1 - (bottom_margin + top_margin)  # height of axes
    ax = fig.add_axes([x, y, w, h])
    y_label_x = 0
    y_label_y = y + h / 2.0
    ax.set_ylabel(y_label, verticalalignment="top", horizontalalignment="center")
    # Horizontally, the "top" of the y axis label is `label_padding` from
    # from the left edge of the figure, no matter what.
    ax.yaxis.set_label_coords(y_label_x, y_label_y, transform=fig.transFigure)
    ax.set_xlabel(x_label)
    d = datetime.datetime.now()
    ax.annotate(
        f'{d.strftime("%I:%M %p %Z %A, %B %d, %Y")}',
        xy=(0.01, 0.01),
        xytext=(0.01, 0.01),
        textcoords="figure fraction",
        xycoords="figure fraction",
        fontsize=10,
        color="0.5",
    )
    return fig, ax


prepare_plot()
