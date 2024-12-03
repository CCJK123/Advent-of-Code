import importlib
import shutil
import sys


def exit_with_msg(exit_code: int, message: str):
    print(message)
    sys.exit(exit_code)


def main():
    # Get puzzle solution to run
    year = 2015
    day = input("Run which day's code? (1-25): ").zfill(2)
    try:
        int(day)
    except ValueError:
        exit_with_msg(1, "That is not a number!")
    if int(day) not in range(1, 26):
        exit_with_msg(1, "That is not a valid number!")

    # Import puzzle solution
    try:
        solution = importlib.import_module(f"{year}.{day}")
    except ModuleNotFoundError:
        prompt = input(
            "Module containing puzzle solution does not exist. Create from template? [Y/n]: "
        )
        if prompt == "" or prompt[0] in ("Y", "y"):
            shutil.copyfile(
                "solutions/python/template.py", f"solutions/python/{year}/{day}.py"
            )
            exit_with_msg(0, f"File `solutions/python/{year}/{day}.py` created.")
        else:
            exit_with_msg(0, "Aborted.")

    # Run puzzle solution with corresponding input
    with open(f"inputs/{year}/{day}.txt", "r") as fp:
        input_str = fp.read()
        outputs = solution.run(input_str)
    if outputs in (None, []):
        print("The code does not return anything!")
    else:
        for i in range(len(outputs)):
            print(f"Part {i+1}: {outputs[i]}")


if __name__ == "__main__":
    main()
