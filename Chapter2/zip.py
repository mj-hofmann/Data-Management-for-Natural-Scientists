# specify lists of users and directories
users = ["Alexander", "Matthias"]
directories = ["productive", "test"]

# loop list simultaneously
for u, d in zip(users, directories):
    # show information
    print(f"Data of user {u} are saved to directory {d}.")