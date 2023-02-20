# import for folder management
import os
# for data handling
import pandas as pd
# moving files, etc
import shutil
# import custom module from "surface_tension" package
from surface_tension import file_to_data
from surface_tension import data_to_information


# get current directory 
current_dir = os.getcwd()
# derive path to data from current diretory of the script
path_to_data = current_dir + os.sep + "raw_from_machine"

# define output folder names
path_to_figure_export = os.getcwd() + os.sep + "_export_figures"
path_to_data_export = os.getcwd() + os.sep + "_data"
path_to_information_export = os.getcwd() + os.sep + "_information"
path_to_parameters_export = os.getcwd() + os.sep + "_parameters"
path_to_raw_archive = os.getcwd() + os.sep + "raw_archive"

# for each export path: make path if if does not exist
for _p in [path_to_figure_export, path_to_data_export,\
           path_to_information_export, path_to_raw_archive,\
           path_to_parameters_export]:
    # check if path exists
    if not os.path.exists(_p):
        # make folder
        os.mkdir(_p)
        # info
        print(_p, "generated.")

#
# Loop files in raw data folder
for file in os.listdir(path_to_data):
    # info
    print("Processing file", file)

    #
    # 1) Read
    _raw_string = file_to_data.read_file_content_as_string(
        path_to_data + os.sep + file
        )
    
    #
    # 2) Get and save data
    # get data
    data = file_to_data.get_data_from_experimental_string(
        _raw_string,
        show_info=False
        )
    # save data
    data.to_csv(
        path_to_data_export + os.sep + file,
        index=False  # do not export index
        )
    
    #
    # 3) Get and save information
    # get information
    information = file_to_data.get_information_from_experimental_string(
                _raw_string,
                show_info=False
                )    
    # ddd further "known" paramwters not captured in the results file
    information = file_to_data.add_further_information(
                information,
                medium="water",
                temperature=23
                )
    # save information
    information.to_csv(
        path_to_information_export + os.sep + file,
        index=False  # do not export index
        )
    
    # get CMC as a parameter (also on information level)
    cmc = data_to_information.get_cmc(
        data,
        gradient_threshold=-20,  # set threshold here
        show_info=False
        )
    # add cmc to "parameters" DataFrame and save it
    parameters = pd.DataFrame({"cmc_g_l" : cmc}, index=[0])
    parameters.to_csv(
        path_to_parameters_export + os.sep + file,
        index=False  # do not export index
        )    
    
    #
    # 4) Optional: Save plots for visual inspection ("quality control")
    data_to_information.plot(
        data,
        file.replace(".csv", ""),  # clean file name withoue extension
        cmc=cmc,
        export_path=path_to_figure_export
        )

    #
    # 5) Move file from raw data folder to raw data archive
    # define filename in archive folder
    file_in_archive = path_to_raw_archive + os.sep + file
    # move only if no file of the same name in archive
    if not os.path.exists(file_in_archive):
        # move raw file there
        shutil.move(
            path_to_data + os.sep + file,
            file_in_archive
            )
    else:
        # info
        print("File", file, "alredy exists in", path_to_raw_archive)