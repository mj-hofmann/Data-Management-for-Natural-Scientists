# %% 1) read csv files

# import for data handling
import pandas as pd

# read data
data = pd.read_csv("_DATA.csv")
# read parameters
parameters = pd.read_csv("_PARAMETERS.csv")


# %% 2) select relevant "data"

# define selection criterion: number of observations per sample
number_of_observations = data.groupby(by="id").count().iloc[:,0]

# get names of samples meeting our criterion / "subsetting"
target_samples = number_of_observations[
                    number_of_observations >= 8
                    ].index.to_list()

# print names of samples meeting the criterion
print("TARGET SAMPLES:")
for _s in target_samples:
    print("  -", _s)


# %% 3) join to "parameters"

# boil down "data" to relevant part
data = data[data["id"].isin(target_samples)]

# merge "data" and "parameters" to "selection"
selection = pd.merge(
    data,  # "left" DataFrame
    parameters,  # "right" DataFrame
    left_on="id",  # id of left df to merge on
    right_on="id",  # id of right df to merge on
    validate="many_to_one"  # optional!
    )

# %% 4) visualize

# import plotting library
import seaborn as sns
import matplotlib.pyplot as plt

# define 1 x 2 plot grid
fig, (ax1, ax2) = plt.subplots(1, 2)
# set figure size
fig.set_size_inches(8, 4)

# barplot of CMCs ("parameter" level)
sns.barplot(
    data=selection,
    y="id",  # use "id" column value as y-axis --> horizontal bars
    x="cmc_g_l",
    palette="Blues",
    ax=ax1  # place plot in "left" space
    )

# lineplot of surface tension isotherms ("data" level)
sns.lineplot(
    data=selection,
    x="concentration_g_l",
    y="surface_tension_mN_m",
    hue="id",  # color by "id" column value
    palette="Blues",
    marker="o",
    ax=ax2  # place plot in "right" space
    )

# set log scaling on x-axis
ax2.set_xscale("log")

# set labels
ax1.set_xlabel("CMC / [g/L]")
ax2.set_xlabel("Concentration / [g/L]")
ax2.set_ylabel("Surface Tension / [mN/m]")

# add common title
plt.suptitle("Surface Tension Isotherm data and CMC values for \
samples measured at >= 8 concentrations")

# hide legend title
plt.legend(title=None)

# adjust suplot sizes to fit them the plot area
fig.tight_layout()

# save figure
fig.savefig(
    "pandas_seaborn_way.png",
    dpi=300
    )