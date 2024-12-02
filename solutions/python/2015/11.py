def run(input_str):
    """Honestly, this day's challenge is probably faster to do manually"""

    # Initial setup
    import re

    outputs = []

    # Parts 1 & 2 Combined
    def generate(password_old):
        while True:
            # Increment password
            password_new = ""
            while password_old != "":
                if password_old[-1] == "z":
                    password_new = "a" + password_new
                    password_old = password_old[:-1]
                else:
                    password_new = (
                        password_old[:-1]
                        + chr(ord(password_old[-1]) + 1)
                        + password_new
                    )
                    password_old = ""
            password_old = password_new
            # Test password
            try:
                assert re.search(r"^[^iol]+$", password_old) is not None
                assert re.search(r"(.)\1.*((?!\1).)\2", password_old) is not None
                has_triplet = False
                for i in range(ord("a"), ord("x") + 1):
                    if (chr(i) + chr(i + 1) + chr(i + 2)) in password_old:
                        has_triplet = True
                        break
                assert has_triplet
                break
            except:
                pass
        return password_new

    password = input_str
    for i in range(2):
        password = generate(password)
        outputs.append(password)

    return outputs
