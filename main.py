year_no = 2022
day_no = input("Run which day's code? ")

try:
    day_no = int(day_no)

except ValueError:
    print("That is not a number!")

else:
    if day_no in range(1, 26):

        day_str = f"day_{str(day_no).zfill(2)}"
        year_str = f"year_{year_no}"

        exec(f"from {year_str}.code.{day_str} import {day_str}")
        with open(f"{year_str}/inputs/{day_str}_input.txt", "r") as fp:
            input_str = fp.read()
            outputs = eval(f"{day_str}(input_str)")

        if outputs in (None, []):
            print("The code does not return anything!")
        else:
            for i in range(len(outputs)):
                print(f"Part {i+1}: {outputs[i]}")

    else:
        print("That is not a valid number!")
