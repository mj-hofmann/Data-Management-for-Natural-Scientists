# define an empty dictionary
my_dict = dict()

# introduce information to dict
my_dict["name"] = "Matthias"
my_dict["training"] = "chemistry"
my_dict["favorite number"] = 8

# loop through only "keys"
for _key in my_dict.keys():
    # info
    print("  -", _key)
    
# loop through only "values"
for _val in my_dict.values():
    # info
    print(_val)
    
# loop through both "keys" and "values"
for _key, _val in my_dict.items():
    # info
    print(_key, ":", _val)
    
# access the "name" specified in the dictionary "my_dict"
print("The name is", my_dict["name"])

# remove a key-value pair
del my_dict["favorite number"]  