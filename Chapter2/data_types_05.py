# define a tuple
my_tuple = ("a", "b", "c")

# get second item via indexing
print("Second item is", my_tuple[1])

# add further letters to the tuple
my_tuple += ("d", "e")

# add one more letter to the tuple one by one
my_tuple += ("f",)
my_tuple += tuple("g")

# add another letter (long version of "+="-notation)
my_tuple = my_tuple + tuple("x")

# print last 4 items in the list / "slicing" to show the introdcued 
# change (modified tuple)
print(my_tuple[-4:])

# change type to list in order to make changes
my_list = list(my_tuple)

# make the change/correction: letter #8 is "h"
my_list[7] = "h"

# get back to immutable tuple --> get tuple from list and overwrite
# existing tuple
my_tuple = tuple(my_list)