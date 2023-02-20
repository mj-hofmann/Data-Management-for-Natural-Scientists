# import for folder management
import os

# get current directory 
current_dir = os.getcwd()
# derive path to data starting from current directory of the script
path_to_data = current_dir + os.sep + "raw_from_machine"

# define output folder name
path_to_figure_export = os.getcwd() + os.sep + "_export_figures"
# make path if it does not exist
if not os.path.exists(path_to_figure_export):
    # make folder/directory
    os.mkdir(path_to_figure_export)

# loop path to data to show list of files
for file in os.listdir(path_to_data):
    # show filename
    print(file)
    
    # use filename without extension as sample name
    sample=file.split(".csv")[0]
    
    # get full filename including path
    file_path = path_to_data + os.sep + file


# %% 1) Read Experimental File content, i.e. "data"

# import custom modules "file_to_data" and "data_to_information"
# modules from "surface_tension" package
from surface_tension import file_to_data
from surface_tension import data_to_information

# get file content as string
file_content_string = file_to_data.read_file_content_as_string(
                                                            file_path
                                                            )

# extract "data" from file content
data = file_to_data.get_data_from_experimental_string(
            file_content_string,
            show_info=False
            )   

# get CMC
cmc = data_to_information.get_cmc(data, show_info=False)

# plot
data_to_information.plot(
        data, 
        sample,  # sample name
        cmc=cmc,  # add CMC information
        export_path=path_to_figure_export  # target directory
        )

# remove no longer required variables
del file_path, file_content_string