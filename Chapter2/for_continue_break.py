# list of examples
my_list = ["hammer", "nail", "saw", "screw driver"]

# go over list
for tool in my_list:
    
    # go to next tool, if tool is "nail"
    if tool == "nail":
        # go to next tool in the list
        continue

    # end for loop, if tool is "saw"
    if tool == "saw":
        break
    
    # print name of tool in any other case
    print(tool)