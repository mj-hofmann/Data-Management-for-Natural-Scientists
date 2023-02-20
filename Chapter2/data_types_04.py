# import the "pandas" module as alias "pd"
import pandas as pd

# create the empty pd.DataFrame "my_dataframe"
my_dataframe = pd.DataFrame()

# add columns "x" and "y"
my_dataframe["x"] = [10, 20, 30, 40, 50]
my_dataframe["y"] = [0.02, 0.10, 0.28, 0.31, 0.34]

# # alternatively: creation of DataFrame from dictionary
# my_dataframe = pd.DataFrame({
#          "x" : [10, 20, 30, 40, 50],
#          "y" : [0.02, 0.10, 0.28, 0.31, 0.34]    
#         })

# get column names
print("my_dataframe consists of columns", my_dataframe.columns)

# get information on row count
print(f"my_dataframe consists of {len(my_dataframe)} rows.")

# introduce a modified column
my_dataframe["x_plus_offset"] = my_dataframe["x"] + 5

# consider only point where "x_plus_offset" is below "44"
my_selection = my_dataframe.query("x_plus_offset < 44")

# make a scatterplot of "x_plus_offset" against "y"
my_selection.plot(
    x="x_plus_offset",  # column name of x-variable
    y="y",  # column name of y-variable
    kind="scatter"
    )

# import plotting module
import matplotlib.pyplot as plt

# labelling of axes
plt.xlabel("x plus offset")
plt.ylabel("Value of y")

# make a barplot of "x_plus_offset" against "y"
my_selection.plot(
    x="x_plus_offset",
    y="y",
    kind="bar"
    )

# get current figure
fig = plt.gcf()

# set size
fig.set_size_inches(4.5,3)

plt.savefig(
    "plot_from_dataframe_scatter.png",
    bbox_inches="tight",
    dpi=300
    )


