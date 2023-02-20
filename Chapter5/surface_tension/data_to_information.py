import matplotlib.pyplot as plt
import numpy as np
import os


#
# plot surface tension isotherm data 
#
def plot(data, sample, cmc=None, export_path=None, show_info=True):
    """
    plot surface tension isotherm data and optionally CMC value

    Parameters
    ----------
    data : pd.DataFrame
        surface tension as obtained from file_to_data's function
        get_data_from_experimental_string.
    cmc : float | int, optional
        CMC value to be highlighted as vertical line. 
        The default is None.
    show_info : bool, optional
        flag for showing intermediate processing results. 
        The default is True.

    Returns
    -------
    None.

    """

    # specify column names to be plotted on x- and y-axes
    x = "concentration_g_l"
    y = "surface_tension_mN_m"

    # plot "guide to the eye"
    plt.plot(
        data[x],  # data on x-axis
        data[y],  # data on y-axis
        "k-",  # solid (-) line without marker in black (k) color
        alpha=0.1  # opacity
        )
    
    # plot data as points
    plt.plot(
        data[x],  # data on x-axis
        data[y],  # data on y-axis
        marker="o",  # set marker symbol
        linestyle=" "  # no connecting lines
        )
    
    # optional plot of CMC as vertical line
    if cmc:
        # vertical line
        plt.axvline(cmc, color="red")

    # add - better formatted - axes labels
    plt.xlabel(x.replace("_", " "))
    plt.ylabel(y.replace("_", " "))
    
    # logarithmic scaling on x-axis
    plt.xscale("log")

    # add legend
    plt.legend()

    # add title
    plt.title(sample)

    # save image, if path specified
    if export_path:      
        # save figure with base filename but other extension --> png
        plt.savefig(
            export_path + os.sep + sample + ".png",
            bbox_inches="tight"  # get rid of whitespace
            )

    # show plot
    plt.show()
    
    # return
    return


#
# extract CMC value
#
def get_cmc(data, show_info=True):
    """
    extract CMC value from DataFrame

    Parameters
    ----------
    data : pd.DataFrame
        surface tension as obtained from file_to_data's function
        get_data_from_experimental_string.
    show_info : bool, optional
        flag for showing intermediate processing results. 
        The default is True.

    Returns
    -------
    CMC as float.

    """
    
    # specify relevant column names for the analytical task
    x = "concentration_g_l"
    y = "surface_tension_mN_m"

    # get gradient
    gradient = np.gradient(
        data[y],  # x-axis data
        data[x]  # y-axis data
        )

    # add "gradient" column to pd.DataFrame "data"
    data["gradient"] = gradient
    
    # info
    if show_info:
        print(data)
    
    # drill down to "data of interest" as doi
    # discard rows with gradient value above threshold, i.e.
    # restrict to rows with gradient below threshold
    doi = data.query("gradient < -1")
    
    # select topmost remaing row
    doi = doi.head(1)

    # assume CMC as measured concentration from doi
    cmc = float(doi[x])
    # info
    if show_info:
        print("-->", cmc)
    
    # return CMC-value
    return cmc