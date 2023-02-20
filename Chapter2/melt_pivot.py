# import
import pandas as pd
 
# build exemplary "original" DataFrame
data_original = pd.DataFrame({
            "sample"            : ["A", "B", "C"],
            "mass_at_5min_g"    : [110, 108, 111],
            "mass_at_15min_g"   : [104, 105, 92]
            })

# print
print(data_original)

# "melt" original DataFrame (== "columns to rows")
data_melted = data_original.melt(
            id_vars="sample",
            value_vars=["mass_at_5min_g", "mass_at_15min_g"]
            )
# print
print(data_melted)

# "pivot" melted DataFrame (== "rows to columns")
data_melted_and_pivoted = data_melted.pivot(
            index="sample",
            columns="variable",
            values="value"
            )
# add index information as "sample" column
data_melted_and_pivoted["sample"] = data_melted_and_pivoted.index
# info
print(data_melted_and_pivoted)