# module for handling SQLite
import sqlalchemy

# create connection to the on-disk database "surface_tension.db"
engine = sqlalchemy.create_engine(
            'sqlite:///surface_tension.db',
            echo=True
            )

# create bound metadata
metadata = sqlalchemy.MetaData(engine)


# %% define tables "data", "information" and "parameters"

from sqlalchemy import Column

# define two column table "parameters"
table_parameters = sqlalchemy.Table(
    "parameters",  # table name
    metadata,  # corresponding metadata
    Column("cmc_g_l", sqlalchemy.Float),
    Column("id", sqlalchemy.Unicode(255), primary_key=True)
    )
# create the table if not exist
table_parameters.create(checkfirst=True)

# define columns of table "information"
table_information = sqlalchemy.Table(
    "information",  # table name
    metadata,  # corresponding metadata
    Column("Device", sqlalchemy.Unicode(255)),
    Column("Device_ID", sqlalchemy.Unicode(255)),
    Column("Experimental_temperature_degree_C]", sqlalchemy.Float),
    Column("File_processed_by", sqlalchemy.Unicode(255)),
    Column("File_processed_on", sqlalchemy.DateTime),
    Column("Measurement_performed_on", sqlalchemy.DateTime),
    Column("Operator", sqlalchemy.Unicode(255)),
    Column("Sample", sqlalchemy.Unicode(255)),
    Column("Solvent_medium", sqlalchemy.Unicode(255)),
    Column("id", sqlalchemy.Unicode(255), 
           sqlalchemy.ForeignKey("parameters.id"))
    )
# create the table if not exist
table_information.create(checkfirst=True)

# define three column table "data"
table_data = sqlalchemy.Table(
    "data",  # table name
    metadata,  # corresponding metadata
    Column("concentration_g_l", sqlalchemy.Float),
    Column("surface_tension_mN_m", sqlalchemy.Float),
    Column("id", sqlalchemy.Unicode(255),
           sqlalchemy.ForeignKey("parameters.id"))
    )
# create the table if not exist
table_data.create(checkfirst=True)


# %% inspect table

# define "inspector"
inspector = sqlalchemy.inspect(engine)

# get table names
table_names = inspector.get_table_names()

# information
print("\nTables in sqlite-database:")
# loop table names
for _table in table_names:
    # print
    print("  -", _table)
    

# %% get and insert "PARAMETERS"

import pandas as pd

# read parameters file
parameters = pd.read_csv("_PARAMETERS.csv")

# loop rows:
for _idx, _row in parameters.iterrows():
    # info
    print(_row)
    
    # define insert statement into sqlalchemy.sql.schema.Table
    # named "table_parameters"
    insert_parameters = table_parameters.insert(values={
            "id"        : _row["id"],
            "cmc_g_l"   : _row["cmc_g_l"] 
            })
    # execute insert statement
    insert_parameters.execute()
    
# check contents of "parameters" table via pandas
parameters_from_sqlite = pd.read_sql_table("parameters", engine)
# print table
print(parameters_from_sqlite)


# %% get and insert "DATA" and "INFORMATION"

# read data file
data = pd.read_csv("_DATA.csv")

# loop rows:
for _idx, _row in data.iterrows():    
    # define insert statement
    insert_data = table_data.insert(values=_row)
    # execute insert statement
    insert_data.execute()
    

# read information file
information = pd.read_csv("_INFORMATION.csv")
# reshape read DataFrame
information = information.pivot(
         index="id", 
         values="value", 
         columns="parameter"
         )
# use index column as "regular column"
information = information.reset_index(level=0)
# ensure datetime format
for _c in ["File processed on", "Measurement performed on"]:
    # convert to datetime
    information[_c] = pd.to_datetime(information[_c])
# rename columns to match names of "table_information" (sqlalchemy)
information.columns = [i.replace(" ", "_")
                       for i in information.columns]

# loop rows:
for _idx, _row in information.iterrows():    
    # define and execute insert statement ("method chaining")
    table_information.insert(values=_row).execute()
    
    
# %% get selected data
#

# define query
query = sqlalchemy.sql.select([ # what do we want?
                                table_data,  # all columns
                                table_parameters.c.cmc_g_l  # CMC only
                                ]).where(
            sqlalchemy.sql.and_( # which conditions should apply?
                table_data.c.id == table_parameters.c.id,
                table_parameters.c.cmc_g_l <= 0.08,
                )
            )

# get DataFrame corresponding to query
query_results = pd.read_sql(query, engine)
# show
print(query_results)
#      concentration_g_l  surface_tension_mN_m                 id   cmc_g_l
# 0             0.004732                 56.57  Polysorbate60.csv  0.052587
# 1             0.004732                 56.57  Polysorbate60.csv  0.052587
# 2             0.004732                 56.57  Polysorbate60.csv  0.052587
# 3             0.004732                 56.57  Polysorbate60.csv  0.052587
# 4             0.004732                 56.57  Polysorbate60.csv  0.052587
# ..                 ...                   ...                ...       ...

# another plotting module
import seaborn as sns
import matplotlib.pyplot as plt

# plot
sns.lineplot(
    x="concentration_g_l",
    y="surface_tension_mN_m",
    hue="id",
    palette="Paired",
    data=query_results,
    marker="o"
    )

# set labels
plt.xlabel("Concentration / [g/l]")
plt.ylabel("Surface tension / [mN/m]")
# get axes
ax = plt.gca()
# set axes scaling
ax.set_xscale("log")

# add vertical guide to the eye at each distinct CMCs
for _cmc in query_results.cmc_g_l.unique():
    ax.axvline(
        _cmc, 
        color="black", 
        linestyle="--",
        linewidth=0.5, 
        alpha=0.3  # opacity
        )
    
# save
plt.savefig(
    "selected_sns_plot.png",
    bbox_inches="tight",
    dpi=300
    )


# %% join data and information

# build join
j = table_data.join(table_parameters).join(table_information)

# build query to select specific columns from joined tables
query = sqlalchemy.sql.select([
        table_data,  # all columns from table "data"
        table_information.c.Operator  # "value" column from 
                                          # "information"
        ]).select_from(j)

# get corresponding DataFrame
query_results = pd.read_sql(query, engine)
# show
print(query_results)

# plot
sns.lineplot(
    data=query_results,
    x="concentration_g_l",
    y="surface_tension_mN_m",
    hue="Operator",  # color by operator
    style="id",  # unique linestyle for each sample
    palette="Paired",
    markers=True,
    units="id",  # what is an "individual" plot
    estimator=None,  # no aggregation as mean, etc.
    )

# set labels
plt.xlabel("Concentration / [g/l]")
plt.ylabel("Surface tension / [mN/m]")

# get axes
ax = plt.gca()
# set axes scaling
ax.set_xscale("log")

# save
plt.savefig(
    "data_by_operator_sns_plot.png",
    bbox_inches="tight",
    dpi=300
    )