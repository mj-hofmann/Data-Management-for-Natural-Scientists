# define function "say_hello"
def say_hello():
    # carry of the functions task
    print("Hello (from the frunction).")
    # return
    return

# call the function
say_hello()

# say hello 5 times
print("Hello from loop:")
for i in range(5):
    # call function
    say_hello()
    

# define properly formatted and documented function
def double_value(value, show_info=True):
    """
    returns the double value of parameter "value" if possible, 
    else None.

    Parameters
    ----------
    value : int, float
        value to be doubled.
    show_info : bool, optional
        flag for showing additional information during function run.
        The default is True.

    Returns
    -------
    doubled_value : 
        doubled value of input "value"
    doubled_value_type :
        type of "doubled_value"
        
    If not appropriate input type (other than int, float), 
    return None
    """
    
    # check type of "value" input
    if type(value) not in [float, int]:
        # Info-Message
        print("Please, use input arguments of type int or float.")
        # no doubling possible --> "leave" function here / exit from
        # this function with return value "None"
        return
        
    # "else"-behavior, if doubling is possible
    doubled_value = 2*value
    doubled_value_type = type(doubled_value)
    
    # info
    if show_info:
        print("result:", doubled_value)
    
    # return doubled value and its type
    return doubled_value, doubled_value_type


# run "double_value" function with different arguments
double_value(4)
double_value("4 bananas")
# call "double_value" function and store return in variable "result"
result = double_value(2.71, show_info=False)

# get "value" from variable named "results" of type "tuple"
print("Value:", result[0])
# get "type" from variable named "results" of type "tuple"
print("Type: ", result[1])