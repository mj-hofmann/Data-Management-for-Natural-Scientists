# define an empty list named "shopping_list"
shopping_list = list()
# append items to the list
shopping_list.append("shoes")
shopping_list.append("hat")
shopping_list.append("3 light bulbs")
shopping_list.append("bananas")

# info on number of items on the list
print(f"There are {len(shopping_list)} items on the shopping list.")


# define a list with all items
my_lotto_numbers_list = [13, 15, 8, 38, 2, 17]

# information setup
print("My lotto numbers are:")

# loop through the list of numbers
for number in my_lotto_numbers_list:
    # print the number
    print("  -", number)
    
# remove "looping variable" named "number"
del number

# loop through the list of numbers ("pythonic")
print("My lotto numbers are:")
[print(f"  - {number}") for number in my_lotto_numbers_list]    


# access the first item on the "shopping list"
first_item = shopping_list[0]
# info
print("The first item on the list is:", first_item)

# loop through the list of numbers via "enumerate"
for idx, number in enumerate(my_lotto_numbers_list):
    # print the index and number
    print(f"Ball #{idx+1}: {number}")