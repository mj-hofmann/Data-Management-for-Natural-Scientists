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
    data : pd.DataFramne
        data abtained from 
        file_to_data.get_data_from_experimental_string.
    sample : str
        title of the generated plot
    cmc : float | int, optional
        characteristic concentration visualized by a vertical
        line. The default is None.
    show_info : bool, optional
        Flag for showing information. The default is True.

    Returns
    -------
    None.

    """

    # specify column names to be used as x- and y-axes
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
    plt.xlabel("Concentration / [g/L]")
    plt.ylabel("Surface Tension / [mN/m]")
    
    # logarithmic scaling on x-axis
    plt.xscale("log")

    # add title
    plt.title(sample)
    
    # get figure
    fig=plt.gcf()
    
    # set image size
    fig.set_size_inches(2.5, 3)

    # save image, if path specified
    if export_path:      
        # save figure with base filename but other extension --> png
        plt.savefig(
            export_path + os.sep + sample + ".png",
            bbox_inches="tight",  # show axis lables "properly" --> formatting
            dpi=300  # set resolution
            )      

    # show plot
    plt.show()
    
    # return
    return


#
# extract CMC value
#
def get_cmc(data, gradient_threshold=-1, show_info=True):
    """
    extract CMC value from DataFrame

    Parameters
    ----------
    data : pd.DataFramne
        data abtained from 
        file_to_data.get_data_from_experimental_string.
    gradient_threshold: int, float
        gradient threshold above which values are discarded
    show_info : bool, optional
        Flag for showing information. The default is True.

    Returns
    -------
    CMC as float.

    """
    
    # specify column names to be used as x- and y-axes
    x = "concentration_g_l"
    y = "surface_tension_mN_m"

    # get gradient
    gradient = np.gradient(
        data[y],  # x-axis data
        data[x]  # y-axis data
        )

    # add "gradient" column to data
    data["gradient"] = gradient
    
    # info
    if show_info:
        print(data)
    
    # drill down to "data of interest" as doi
    # discard rows with gradient value below threshold
    doi = data.query("gradient < @gradient_threshold")
    
    # select topmost remaing row
    doi = doi.head(1)

    # assume CMC as measured concentration from doi
    cmc = float(doi[x])
    # info
    if show_info:
        print("-->", cmc)
    
    # return CMC-value
    return cmc