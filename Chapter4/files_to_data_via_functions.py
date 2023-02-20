# import custom module from package "surface_tension"
from surface_tension import file_to_data

# specify file name
file = "Polysorbate40.csv"

# 1) Read experimental file content
file_content_string = file_to_data.read_file_content_as_string(file)

# 2.1) Extract "data" from file content
data = file_to_data.get_data_from_experimental_string(
            file_content_string,
            show_info=False
            )   

# 2.2) Extract "parameters" from file content
information = file_to_data.get_information_from_experimental_string(
            file_content_string,
            show_info=False
            )

# 2.3) Add further "known" parameters not captured in the results 
# file
information = file_to_data.add_further_information(
            information,
            medium="water",
            temperature=23
            )

# remove no longer required variables from the script
del file, file_content_string