# import
import pandas as pd
 
# build individual DataFrames to be merged
data_A = pd.DataFrame({
            "A"          : ["A", "B", "C"],
            "c_A"        : [1, 2, 3]
            })

data_B = pd.DataFrame({
            "B"         : ["A", "E", "B"],
            "c_B"       : [2, 8, 4]
            })

# print original DataFrames
print("data_A")
print(data_A)
print("data_B")
print(data_B)

# merge DataFrames on columns "A" and "B"
data_merged = pd.merge(
        data_A,  # "left" DataFrame
        data_B,  # "right" DataFrame
        left_on="A",  # column on which left DataFrame is merged
        right_on="B",  # column on which right DataFrame is merged,
        how="inner"
        )
# print merged DataFrame
print("data_merged")
print(data_merged)