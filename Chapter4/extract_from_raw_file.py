# define filename
file = "Polysorbate40.csv"

# initialize results variable of type string (empty)
results = ""

# open the file for reading "r" with encoding utf-8
with open(file, "r", encoding="utf-8") as f:
    # read file line by line
    while True:
        # read line
        line = f.readline()
        # append to string
        results = results + line
        # end of file reached?
        if not line:
            print(type(line))
            # break infinite while loop
            break


# %% extract data via regex
#

# pattern as derived via "regex101.com"
pattern = "(.*),(\d+.*)"

# import python regex module
import re

# find pattern in string "results"
findings = re.findall(
                pattern,
                results
            )
# show "findings" variable (list of tuples)
print(findings)

# import pandas module to use the DataFrame with alias pd
import pandas as pd

# initialize empty pandas.DataFrame data
data = pd.DataFrame()

# initialize empty list of concentrations
concentration_g_l = []
# loop through findings to get concentrations
for _finding in findings:
    # info
    print(_finding)
    # get the first element of the "_finding" (string) and convert
    # to float
    _c_g_l = float(_finding[0])
    # append extracted concentration to list of concentrations
    concentration_g_l.append(_c_g_l)
    
# use concentration list as column in the defined DataFrame
data["concentration_g_l"] = concentration_g_l

# use surface tension as colums (via list comprehension)
# type conversion to float via "float()"-function
data["surface_tension_mN_m"] = [float(i[1]) for i in findings]

## alterantively: build DataFrame from list of tuples available from
## "findings"
#data =  pd.DataFrame(
#            findings,  # structured source of data
#            columns=[  # specify column names
#                "concentration_g_l", 
#                "surface_tension_mN_m"
#                ], 
#            dtype=float  # force conversion to float
#            )

# print resulting DataFrame
print(data)

# clean variable space
del concentration_g_l, pattern, findings


# %% extract parameters via regex
#

# define regex pattern
pattern = "(?P<parameter>[\w ]+): (?P<value>.*)"

# find pattern in string "results" as iterator "findings_parameters"
findings_parameters = re.finditer(
    pattern,
    results
    )

# initialize list of "parameters" and "values"
parameters = []
values = []

# loop over iterable to get each "parameter" and "value"
for _f in findings_parameters:
    # get dict for this finding
    _dict = _f.groupdict()
    # extract "paramater" and "value" and append to list
    parameters.append(_dict["parameter"])
    values.append(_dict["value"])

# build pd.DataFrame "information" from the extracted list
information = pd.DataFrame({
    "parameter" : parameters,
    "value" : values
    })
    
## alternatively: get "information" DataFrame directly from list
## of tuples
#information =  pd.DataFrame(
#            re.findall(pattern, results),  # structured source of data
#            columns=[  # specify column names
#                "parameter", 
#                "value"
#                ], 
#            dtype=float  # force conversion to float
#            )
    
# remove variables which are no longer required
del parameters, values, findings_parameters, pattern


# %% add further -- considered -- relevant information
#

# import modules for adding further pieces of information
import datetime
import os

# define column names as strings
_par = "parameter"
_val = "value"

# solvent medium (add new row via dict)
information = information.append({
    _par : "Solvent medium",
    _val : "water"
    }, ignore_index=True  # increase index "automatically"
    )
# experimental temperature (add new row via pd.DataFrame)
information = information.append(pd.DataFrame({
    _par : "Experimental temperature degree C",
    _val : 23  # temperature of thermostatted room
    }, index=[len(information)+1])  # increase index explicitly
    )
# processing timestamp (add new row via dict)
information = information.append({
    _val : datetime.datetime.now().replace(microsecond=0),  # timestamp
    _par : "File processed on"
    }, ignore_index=True
    )
# operator (add new row via pd.DataFrame)
information = information.append(pd.DataFrame({
    _val : os.getlogin(),  # get logged in user
    _par : "File processed by"
    }, index=[len(information)+1])
    )
