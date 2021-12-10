day_no = input("Run which day's code? ")

try:
    day_no = int(day_no)

    if day_no in range(1, 26):
        
        day_str = f"day_{str(day_no).zfill(2)}"
        exec(f"from code.{day_str} import {day_str}")
        with open(f"inputs/{day_str}_input.txt", "r") as fp:
            input_str = fp.read()
            outputs = eval(f"{day_str}(input_str)")
        
        if outputs == None:
            print("The code does not return anything!")
        else:
            for i in range(len(outputs)):
                print(f"Part {i+1}: {outputs[i]}")
    
    else:
        print("That is not a valid number!")

except ValueError:
    print("That is not a number!")