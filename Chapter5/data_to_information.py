# import for folder management
import os

# get current directory 
current_dir = os.getcwd()
# derive path to data starting from the current directory of the 
# script
path_to_data = current_dir + os.sep + "raw_from_machine"

# loop path to data to show list of files
for file in os.listdir(path_to_data):
    # show filename
    print(file)
    # get full filename including path
    file_path = path_to_data + os.sep + file


# %% 1) Read Experimental File content, i.e. "data"

# import custom module from "surface_tension" package
from surface_tension import file_to_data

# get file content as string
file_content_string = file_to_data.read_file_content_as_string(
                                                        file_path
                                                        )

# extract "data" from file content
data = file_to_data.get_data_from_experimental_string(
            file_content_string,
            show_info=False
            )   

# remove no longer required variables
del file_path, file_content_string


# %% 2) visualize data

#  import plotting library
import matplotlib.pyplot as plt

# plot
plt.plot(
    data["concentration_g_l"],  # data on x-axis
    data["surface_tension_mN_m"]  # data on y-axis
    )
# show plot
plt.show()

# specify column names to be used as x- and y-axes
x = "concentration_g_l"
y = "surface_tension_mN_m"

# specify label names
x_label = "Concentration / [g/l]"
y_label = "Surface tension / [mN/m]"

# plot "guide to the eye"
plt.plot(
    data[x],  # data on x-axis
    data[y],  # data on y-axis
    color="black",  # black color
    linestyle="-",  # solid line
    alpha=0.1  # opacity
    )

# plot data as points
plt.plot(
    data[x],  # data on x-axis
    data[y],  # data on y-axis
    marker="o",  # set marker symbol
    linestyle=" "  # no connecting lines
    )

# add - better formatted - axes labels
plt.xlabel(x_label, size=14)
plt.ylabel(y_label, size=14)

# logarithmic scaling on x-axis
plt.xscale("log")

# import module for handling dates
import datetime

# add timestamp of processing
plt.text(
    0.1, 
    data[y].max()-1, 
    f"Timestamp:\n{datetime.datetime.now().replace(microsecond=0)}"
    )

# add title
plt.title(file)

# define output folder name
path_to_figure_export = os.getcwd() + os.sep + "_export_figures"
# create export path if it does not exist
if not os.path.exists(path_to_figure_export):
    # make folder
    os.mkdir(path_to_figure_export)

# save figure with base filename but other extension --> png
plt.savefig(
    path_to_figure_export + os.sep + file.replace(".csv", ".png"),
    bbox_inches="tight",  # remove whitespace around figure
    dpi=300  # set resolution
    )

# show plot
plt.show()


# %%  3) get " state of the art " parameters

# module for calculating gradient (among others)
import numpy as np

# get gradient
gradient = np.gradient(
    data[y],  # y-axis data
    data[x]   # x-axis data
    )

# initialize figure
fig, ax = plt.subplots()

# introduce second axis
ax_gradient = ax.twinx()

# plot data as points on "ax"
ax.plot(data[x], data[y], "ko")
# add gradient on "ax_gradient" (secondary y-axis)
ax_gradient.plot(data[x], gradient, "rs-")

# logarithmic scaling on x-axis
plt.xscale("log")

# add - better formatted - axes labels
ax.set_xlabel(x_label, size=14)
ax.set_ylabel(y_label, size=14)
ax_gradient.set_ylabel(
                "Gradient of surface tension\n / [(mN/m)/(g/l)]",
                size=14
                )

# add "gradient" column to data
data["gradient"] = gradient

# drill down to "data of interest" as doi
# discard rows with gradient value below absolute threshold, i.e.
# selection of "below CMC" surface tension-concentration value pairs
doi = data.query("gradient < -1")

# select topmost remaing row
doi = doi.head(1)

# assume CMC as measured concentration from doi
cmc = float(doi[x])  # x = "concentration_g_l"

# show value in plot
ax.axvline(cmc, color="green", linestyle="--", label="cmc")

# add legend at location 2 ('upper left')
ax.legend(loc=2)

# save figure with base filename but other extension --> png
plt.savefig(
    path_to_figure_export + os.sep + file.replace(".csv", "_cmc.png"),
    bbox_inches="tight",
    dpi=300
    )

# show plot
plt.show()

# remove no longer required variables
# del fig, ax, ax_gradient
del gradient, doi