import matplotlib as mpl
import matplotlib.pyplot as plt
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
    sns.set_context("talk")
    sns.set_style("whitegrid")
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


prepare_plot()