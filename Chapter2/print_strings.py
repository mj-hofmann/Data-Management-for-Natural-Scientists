# define variables
sport = "Table Tennis"
ball_diameter_mm = 40

# print information using "f-strings"
print(f"The ball diameter in {sport} is {ball_diameter_mm} mm.")

# print information using "str.format"
print("The ball diameter in {} is {} mm.".format(
        sport,
        ball_diameter_mm
        )
    )