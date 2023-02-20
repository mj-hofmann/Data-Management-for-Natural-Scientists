# imports
import pandas as pd

# generate example DataFrame
names = ["Lisa", "Sara", "Michael", "Josef"]
gender = ["f", "f", "m", "m"]
height = [164, 172, 182, 177]
# lists to DataFrame via implicitly defined python dictionary {}
data = pd.DataFrame({
        "name"      : names,
        "gender"    : gender,
        "height_cm" : height,
        })

# get mean height by gender using "groupby"
result = data.groupby(by="gender").mean()
# show results
print(result)

# work with data subsets via iterator
for _gender, _data in data.groupby(by="gender"):
    # info
    print("\nData subset:", _gender)
    print(_data)