# import module for reading data
import pandas as pd

# specify file
file = "Polysorbate40.csv"

# read
raw = pd.read_csv(
            file,
            sep="\n",  # new line separater as column separator
            index_col=0  # use all string as column
            )
# info
print(raw)


# %% get "data" part via index range
#

data = raw.loc[
        "=== COLLECTED DATA ===":
        "=== SUMMARY INFORMATION ===",  # select range of rows
        :  # select all columns
        ]
# info
print(data)
# Empty DataFrame
# Columns: []
# Index: [=== COLLECTED DATA ===, Concentration / [g/L],Surface 
# tension / [mN/m], 4.0790e-01,43.78, 1.4911e-01,43.84, 
# 8.8993e-02,43.78, 3.9720e-02,46.68, 
# 1.9793e-02,49.43, 9.2199e-03,53.69, 
# 2.7936e-03,57.40, === SUMMARY INFORMATION ===]

# use index as column as value column
data = data.reset_index(level=0)
# set name of previous index column to "raw"
data.columns = ["raw"]

# discard first and last row
data = data.iloc[1:-1,:]

# separate columns via list comprehensions; split at ","
data["column_1"] = [i[0] for i in data["raw"].str.split(",")]
data["column_2"] = [i[1] for i in data["raw"].str.split(",")]

# discard "raw" column
data = data.drop(columns=["raw"])

# use first line as header
data.columns = data.iloc[0,:]

# use second to last row as data part
data = data.iloc[1:,:]

# convert column to float
for _c in data.columns:
    data[_c] = data[_c].astype(float)

# show results
print(data)
# 1  Concentration / [g/L]  Surface tension / [mN/m]
# 2               0.407900                     43.78
# 3               0.149110                     43.84
# 4               0.088993                     43.78
# 5               0.039720                     46.68
# 6               0.019793                     49.43
# 7               0.009220                     53.69
# 8               0.002794                     57.40


# %% get "information" part via index range
#

information = raw.loc[
        :"=== COLLECTED DATA ===",  # select range of rows
        :  # select all columns
        ]

# use index as column
information = information.reset_index(level=0)
# set name of previous index column to "raw"
information.columns = ["raw"]

# discard last row
information = information.iloc[:-1,:]

# separate columns via list comprehensions; split at ": "
information["column_1"] = [i[0].strip() for i in 
                               information["raw"].str.split(": ")]
information["column_2"] = [i[1].strip() for i in 
                               information["raw"].str.split(": ")]

# discard "raw" column
information = information.drop(columns=["raw"])

# transpose results
information = information.T

# use first line as header
information.columns = information.iloc[0,:]
# use second to last row as data part
information = information.iloc[1:,:]

# reset index
information = information.reset_index(drop=True)

# show results
print(information.T)
#                                             0
# column_1                                     
# Sample                          Polysorbate40
# Measurement performed on  2022-01-28 13:37:44
# Operator                     Matthias Hofmann
# Device                        Fancy Machine X
# Device ID                            Y0139836