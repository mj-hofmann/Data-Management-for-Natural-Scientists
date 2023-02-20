# module for handling sqlite
import sqlalchemy

# create connection to on disk database "surface_tension.db"
engine = sqlalchemy.create_engine(
            'sqlite:///surface_tension.db',
            echo=True
            )

# create bound metadata
metadata = sqlalchemy.MetaData(engine)
# load all available table definitions from the database.
metadata.reflect()

# define "inspector"
inspector = sqlalchemy.inspect(engine)

# show available tables
for _table_name in inspector.get_table_names():
    # show this table
    print("  -", _table_name)


# %% get tables
#

# access database tables
table_data = metadata.tables["data"]
table_information = metadata.tables["information"]
table_parameters = metadata.tables["parameters"]

# join results
join = table_data\
        .join(table_parameters)\
        .join(table_information)

# specify sqlalchemy query
from sqlalchemy.sql import select
import datetime

query = select([
                table_data,  # get all data columns
                table_parameters.c.cmc_g_l  # get CMC column
                ])\
            .select_from(join)\
                .where(
                    table_information.c.Measurement_performed_on\
                        <= datetime.datetime(2022, 1, 28, 12, 0, 0)
                    )

# import for DataFrame handling
import pandas as pd

# get data corresponding to query
data = pd.read_sql(query, engine)
# show
print(data)

# === Console output: ===
#     concentration_g_l  surface_tension_mN_m                 id   cmc_g_l
# 0            0.004732                 56.57  Polysorbate60.csv  0.052587
# 1            0.008944                 54.14  Polysorbate60.csv  0.052587
# 2            0.019793                 49.89  Polysorbate60.csv  0.052587
# 3            0.030056                 47.73  Polysorbate60.csv  0.052587
# 4            0.043003                 46.37  Polysorbate60.csv  0.052587
# 5            0.052587                 44.74  Polysorbate60.csv  0.052587
# 6            0.088993                 44.67  Polysorbate60.csv  0.052587
# 7            0.149110                 44.58  Polysorbate60.csv  0.052587
# 8            0.406020                 44.60  Polysorbate60.csv  0.052587
# 9            0.004837                 55.50  Polysorbate80.csv  0.040683
# 10           0.019440                 48.00  Polysorbate80.csv  0.040683
# 11           0.025564                 45.99  Polysorbate80.csv  0.040683
# 12           0.033768                 45.81  Polysorbate80.csv  0.040683
# 13           0.040683                 45.47  Polysorbate80.csv  0.040683
# 14           0.057990                 45.52  Polysorbate80.csv  0.040683
# 15           0.086586                 45.43  Polysorbate80.csv  0.040683
# 16           0.147310                 45.56  Polysorbate80.csv  0.040683
# 17           0.402270                 45.41  Polysorbate80.csv  0.040683

# %% plotting
#

# show available columns
for _c in data.columns:
    print(_c)

# import basic plotting library
import matplotlib.pyplot as plt

# loop by sample
for this_sample, this_sample_data in data.groupby(by="id"):
    # info
    print(this_sample)
    print(this_sample_data)
    
    # plot experimental data
    plt.plot(
        this_sample_data["concentration_g_l"],
        this_sample_data["surface_tension_mN_m"],
        marker="o",
        label=this_sample,  # legend entry
        )
    
    # cmc indication line
    plt.axvline(
        this_sample_data["cmc_g_l"].to_list()[0],
        color="black",
        linewidth=0.5
        )

# set axis scaling
plt.xscale("log")

# add legend (filled via "label=" in plot-function calls)
plt.legend()
    
# figure "cosmetics"
plt.xlabel("Concentration / [g/l]", size=14)
plt.ylabel("Surface tension / [mN/m]", size=14)
plt.title("Surface tension isotherms measured before {}".format(
    datetime.datetime(2022, 1, 28, 12, 0, 0),
    ),
    size=20
    )

# save
plt.savefig(
    "sqlalchemy_matplotlib_way.png",
    bbox_inches="tight", # removes extra white space around the figure
    dpi=300  # dots per inch (image quality)
    )