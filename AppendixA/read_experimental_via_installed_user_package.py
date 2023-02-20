# import custom (installed) modules with alias
import surface_tension.file_to_data as st_data
import os

# get current path
path = os.getcwd()
# info
print("script path:", path)
# script path: C:\Users\LocalAdmin\Documents\_Data_and_code\AppendixA

# build path to data
path_to_data = path + os.sep + os.pardir + os.sep + "Chapter5" +\
    os.sep + "raw_from_machine"
# info
print("data path", path_to_data)
# data path C:\Users\LocalAdmin\Documents\_Data_and_code\AppendixA\..
# \Chapter5\raw_from_machine

# loop files
for _file in os.listdir(path_to_data):
    # info
    print(_file)
    # Polysorbate20.csv
    
    # read file as string
    file_str = st_data.read_file_content_as_string(
        path_to_data + os.sep + _file
        )
    # get data from string
    data = st_data.get_data_from_experimental_string(
        file_str,
        show_info=False
        )
    # show top columns of resulting dataframe
    print(data.head())
    #        concentration_g_l  surface_tension_mN_m
    # 0           0.409490                 43.73
    # 1           0.147970                 43.73
    # 2           0.087851                 43.73
    # 3           0.040554                 46.13
    # 4           0.019972                 49.40
    
    # stop after first file
    break