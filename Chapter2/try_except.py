# import DataFrame
from pandas import DataFrame

# define DataFrame to be appended
data_to_append = DataFrame({
    "name" :  ["Walter", "Jesse"],
    "location" : ["Munich", "Berlin"]
    })

# try: append "data_to_append" to so far non-existing "data"
try:
    data = data.append(data_to_append)

# if not successful: define empty "data" and append to this
except Exception as e:
    # print information on Exception
    print(type(e).__name__, e)
    
    # define empty DataFrame (to be appended to)
    data = DataFrame()
    # append "data_to_append" to "data" (initialized empty)
    data = data.append(data_to_append)
    
# info
print(data)