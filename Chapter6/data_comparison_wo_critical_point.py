# import for folder management
import os
# import custom module from "surface_tension" package
from surface_tension import file_to_data
from surface_tension import data_to_information

import matplotlib.pyplot as plt


# get current directory 
current_dir = os.getcwd()
# derive path to data from current diretory of the script
path_to_data = current_dir + os.sep + "raw_archive"

# file to evaluated
file = "Polysorbate80.csv"


#
# 1) Read
_raw_string = file_to_data.read_file_content_as_string(
    path_to_data + os.sep + file
    )

#
# 2) Get and save data
# get data
data = file_to_data.get_data_from_experimental_string(
    _raw_string,
    show_info=False
    )
# get data without "critical" point
critical_point_idx = 6
data_clean = data[data.index != critical_point_idx]

# get CMC as as parameter (also on information level)
cmc = data_to_information.get_cmc(
    data,
    gradient_threshold=-20,
    show_info=False
    )

# plot settings
x = "concentration_g_l"
y = "surface_tension_mN_m"

# define figure
fig, ax = plt.subplots(1, 2)

for _ax_nr, _data in zip(range(2), [data, data_clean]):
    # plot "guide to the eye"
    ax[_ax_nr].plot(
        _data[x],  # data on x-axis
        _data[y],  # data on y-axis
        "k-",  # line without marker in blac"k" color
        alpha=0.1  # opacity
        )
    # plot data as points
    ax[_ax_nr].plot(
        _data[x],  # data on x-axis
        _data[y],  # data on y-axis
        marker="o",  # set marker symbol
        linestyle=" "  # no connecting lines
        )
    # plot cmc
    ax[_ax_nr].axvline(cmc, color="red")
    # set scaling
    ax[_ax_nr].set_xscale("log")
    # cosmetics
    ax[_ax_nr].set_xlabel(x.replace("_", " "))
    ax[_ax_nr].set_ylabel(y.replace("_", " "))
    
# highligt
ax[0].plot(
    data.loc[critical_point_idx, x],
    data.loc[critical_point_idx, y],
    "rs"
    )

# save
plt.savefig(
    "one_point_difference.png",
    dpi=300,
    bbox_inches="tight"
    )
