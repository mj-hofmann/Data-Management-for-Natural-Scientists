# module for handling sqlite
import sqlalchemy

# create connection to on disk database "dummy.db"
engine = sqlalchemy.create_engine(
            'sqlite:///dummy.db',
            echo=True
            )

# create bound metadata
metadata = sqlalchemy.MetaData(engine)


# %% define dummy table "my_table" with comments
#

from sqlalchemy import Column

# define two table "my_table" holding columns "name" and "age"
table = sqlalchemy.Table(
    "my_table",  # table name
    metadata,  # corresponding metadata
    Column("name", 
            sqlalchemy.Float, 
            comment="Name of the user",  # comment on "user" column
            primary_key=True
            ),
    Column("age", 
            sqlalchemy.Unicode(255), 
            comment="Age of the user in years"  # column comment
            ),
    comment="A table holding information on users"  # table comment
    )

# create the table if it does not exist
table.create(checkfirst=True)


# %% get comments on table and columns
#

# information on table
print(f"Table Comment on {table.name}: {table.comment}")

# loop columns and get comments
for _c in table.columns:
    # print column name
    print(f"Column {_c}:")
    # print comment
    print(f"  - Comment: {_c.comment}")

# Table Comment on my_table: A table holding information on users
# Column my_table.name:
#   - Comment: Name of the user
# Column my_table.age:
#   - Comment: Age of the user in years