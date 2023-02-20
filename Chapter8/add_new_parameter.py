# %% 1) read relevant existing SQLite-database tables
#

# module for handling SQLite
import sqlalchemy
# for DataFrame handling
import pandas as pd

# SQLite filename
file_sqlite = "surface_tension.db"

# generate connection to database
engine = sqlalchemy.create_engine(
            "sqlite:///" + file_sqlite,
            echo=True
            )

# create bound metadata
metadata = sqlalchemy.MetaData(engine)

# load all available table definitions from the database.
metadata.reflect()

# define "inspector"
inspector = sqlalchemy.inspect(engine)

# show avaiable table_names
for _table_name in inspector.get_table_names():
    # show this table
    print("  -", _table_name)
    
#  - data
#  - information
#  - parameters
    
# show columns in "parameters" table
for _column in inspector.get_columns("parameters"):
    # print column name
    print("  #", _column["name"])
    
#  # cmc_g_l
#  # id
  
# get "data" as pd.DataFrame
data = pd.read_sql_table("data", engine)
# get "parameters" as pd.DataFrame
parameters = pd.read_sql_table("parameters", engine)

# get "parameters" and "data" as sqlalchemy.Tables
table_parameters = metadata.tables["parameters"]
table_data = metadata.tables["data"]

# return types depending on kind of "table access"
print("data is of type", type(data))
# data is of type <class 'pandas.core.frame.DataFrame'>
print("table_data is of type", type(table_data))
# table_data is of type <class 'sqlalchemy.sql.schema.Table'>


# %% 2) extract "new parameter"
#

# plotting library for visual check
import matplotlib.pyplot as plt

# initialize dict holding the new parameter "minimum surface tension"
parameter_to_add = dict()

# loop samples
for _g, _data in data.groupby(by="id"):
    # info
    print(_g)
    
    # get minimum surface tension value
    min_surf_tension_mN_m = _data[
        "surface_tension_mN_m"
        ].min()
    
    # info
    print(min_surf_tension_mN_m)
    
    # add value to dict
    parameter_to_add[_g] = min_surf_tension_mN_m
    
    # plot for plausibility check
    # all measured points
    plt.plot(
        _data["concentration_g_l"],
        _data["surface_tension_mN_m"],
        marker="o"
        )
    # horizontal (--> h) line to highlight identified 
    # minimum surface tension
    plt.axhline(
        min_surf_tension_mN_m,  # y-value of horizontal line 
        color="red", 
        alpha=0.5  # opacity
        )
    # set to log scale
    plt.xscale("log")
    # add title
    plt.title(_g)
    
    # plot cosmetics
    plt.xlabel("Concentration / [g/l]", size=14)
    plt.ylabel("Surface tension / [mN/m]", size=14)

    # save (last) plot
    plt.savefig(
        "minimum_surface_tension_example.png",
        dpi=300
        )
    
    # show plot
    plt.show()


# %% 3) write modified "parameter" table back to database
#

# module for table modifiaction
import migrate.changeset

# "append" new columns to existing Table
table_parameters.create_column(
    sqlalchemy.Column(
        'minimum_surface_tension_mN_m',
        sqlalchemy.Float
        )
    )

# update values
for key, value in parameter_to_add.items():
    #info
    print("Inserting", value, "for", key)
    # update table
    table_parameters.update().where(
            table_parameters.c.id == key  # at specific row
            ).execute(
                minimum_surface_tension_mN_m=value  # set the value
            )

# remove no longer required variables
del key, value


# %% 4) visualize new findings
#

# join "data" and "parameters" tables according to declared keys
join = table_data.join(table_parameters)

# select
query = sqlalchemy.sql.select([
            table_data,  # use all columns from "data" table
            table_parameters.c.minimum_surface_tension_mN_m,
            table_parameters.c.cmc_g_l  # select CMC column
            ]).select_from(
                join  # used joined tables as "pool" to select from
                )

# get DataFrame corresponding to query
query_data = pd.read_sql(query, engine)


import matplotlib.pyplot as plt
import seaborn as sns

# define 2x1 plot setup
fig, (ax1, ax2) = plt.subplots(1, 2)

# define colour palette to be used
# see https://seaborn.pydata.org/tutorial/color_palettes.html
palette = "Paired"

# scatterplot of minimum surface tension vs CMC
sns.scatterplot(
    data=query_data,
    x="cmc_g_l",
    y="minimum_surface_tension_mN_m",
    hue="id",  # set colour by id
    palette=palette,
    ax=ax1,
    legend=None
    )

# line plot of correponding surface tension isotherms
sns.lineplot(
    data=query_data,
    x="concentration_g_l",
    y="surface_tension_mN_m",
    hue="id", # set colour by id
    palette=palette,
    marker="o",
    ax=ax2
    )

# set logarithmic axes
ax2.set_xscale("log")

# set label explicitly
ax1.set_xlabel("CMC / [g/l]")
ax1.set_ylabel("Minimum surface tension / [mN/m]")
ax2.set_xlabel("Concentration / [g/l]")
ax2.set_ylabel("Surface tension / [mN/m]")

# legend finetuning
plt.legend(
    frameon=False,  # no frame
    fontsize=8  # smaller font size
    )

# save plot
plt.savefig(
    "add_new_parameter.png",
    dpi=300
    )