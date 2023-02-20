# import for folder management
import os
# for data handling
import pandas as pd

# get current directory 
current_dir = os.getcwd()

# specify folders to be looped
path_to_data = os.getcwd() + os.sep + "_data"
path_to_information = os.getcwd() + os.sep + "_information"
path_to_parameters = os.getcwd() + os.sep + "_parameters"

# loop #1 | "outer" loop
# "zip" together folder and file name
for _folder, _target in zip(
        [path_to_data, path_to_information, path_to_parameters],
        ["_DATA.csv", "_INFORMATION.csv", "_PARAMETERS.csv"]
        ):
    # info
    print("Merging contents of", _folder, "to", _target)

    # loop #2 | "inner" loop
    # loop current folder
    for _file in os.listdir(_folder):
        # info
        print("  -", _file)
        # read file contents as pd.DataFrame
        _this_data = pd.read_csv(
            _folder + os.sep + _file
            )
        # add sample or ID information
        _this_data["id"] = _file
        
        # build overall DataFrame
        try:
            data = data.append(_this_data)
        except Exception as e:
            # info
            print(e)
            data = _this_data
            
    # save collected results to csv
    data.to_csv(
        current_dir + os.sep + _target,
        index=False  # do not export index
        )
    
    # info
    print("--> SAVED!\n")
        
    # remove "data" variable
    del data