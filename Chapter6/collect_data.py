# import for folder management
import os
# for data handling
import pandas as pd

# get current directory 
current_dir = os.getcwd()

# specify folder to be looped
path_to_data = os.getcwd() + os.sep + "_data"

# loop folder
for _file in os.listdir(path_to_data):
    # info
    print(_file)
    # read file contents as pd.DataFrame
    _this_data = pd.read_csv(
        path_to_data + os.sep + _file
        )
    # add sample or ID information
    _this_data["id"] = _file
    
    # build overall DataFrame
    try:
        data = data.append(_this_data)
    except:
        data = _this_data

# save collected results to csv
data.to_csv(
    current_dir + os.sep + "_DATA.csv",
    index=False  # do not export index
    )