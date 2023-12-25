def day_12(input_str):
    # Initial setup
    import itertools, math, re

    input_array = tuple(
        tuple([i.split(" ")[0], [int(j) for j in i.split(" ")[1].split(",")]])
        for i in input_str.split("\n")
    )
    outputs = []

    # Part 1
    ## Function to split groups into subgroups
    def split_groups(groups, no_of_groups):
        split_indices_list = itertools.combinations_with_replacement(
            range(len(groups) + 1), no_of_groups
        )
        for split_indices in split_indices_list:
            group_combination, previous_index = [], 0
            for index in split_indices:
                group_combination.append(groups[previous_index:index])
                previous_index = index
            group_combination.append(groups[previous_index:])
            yield group_combination

    ## Function to generate possible spring sequences from groups
    def generate_springs(groups, sequence_length):
        insertions_needed = sequence_length - sum(groups)
        sections_count = len(groups) + 1
        permutations = (
            combination
            for combination in itertools.product(
                range(insertions_needed + 1), repeat=sections_count
            )
            if (sum(combination) == insertions_needed)
            and all(insert_amt >= 1 for insert_amt in combination[1:-1])
        )
        for permutation in permutations:
            possible_spring_sequence = ""
            groups_copy = [*groups, 0]
            for insert_amt in permutation:
                possible_spring_sequence += insert_amt * "." + groups_copy.pop(0) * "#"
            yield possible_spring_sequence

    ## Function to parse sequence of springs (assumes valid springs-groups pair)
    def get_arrangements(springs, groups):
        arrangements = 1
        # print(springs, groups)

        # Verify again to catch errors from recursion
        assert len(springs) >= sum(groups) + len(groups) - 1
        assert groups != [] if "#" in springs else True
        assert springs.count("#") <= sum(groups)

        # Blanket catches
        if groups == []:
            springs = ""
            # print("Type: Blanket (a)")
        elif len(springs) == groups[0] and len(groups) == 1:
            springs, groups = "", []
            # print("Type: Blanket (b)")

        # Handle damaged springs (#)
        ## Remove leading group of damaged springs
        elif re.search(rf"^#[#?]{{{groups[0]-1}}}(?=[^#]|$)", springs) is not None:
            springs = springs[groups[0] + 1 :]
            del groups[0]
            # print("Type: # (a)")
        ## Remove guaranteed operational spring before group of damaged springs
        elif springs[groups[0]] == "#" and springs[0] != "#":
            springs = springs[1:]
            # print("Type: # (b)")

        # Handle unknown springs (?)
        ## Consider arrangements if all springs are unknown
        elif set(springs) == {"?"}:
            arrangements *= math.comb(
                len(springs) - sum(groups) + 1, len(groups)
            )  # Insert groups of damaged springs between operational springs
            springs, groups = "", []
            # print("Type: ?")

        # Handle sequences of damaged and unknown springs (# and ?) (brute force)
        elif set(springs) == {"#", "?"}:
            arrangements = 0
            for possible_spring_sequence in generate_springs(groups, len(springs)):
                if all(
                    possible_spring_sequence[index] == "#" if spring == "#" else True
                    for index, spring in enumerate(springs)
                ):
                    arrangements += 1
            springs, groups = "", []
            # print("Type: # and ?")

        # This shouldn't trigger
        else:
            raise Exception

        # Check if all groups accounted for
        if springs != "" or groups != []:
            arrangements = get_arrangements(springs, groups)
        # print(springs, groups, arrangements)
        return arrangements

    ## Main code
    total_arrangements = 0
    for springs, groups in input_array:
        row_arrangements = 0

        # print("=" * 20)
        # print(springs, groups)

        # Handle operational springs (.)
        assert type(springs) == str
        ## Remove leading and trailing operational springs
        springs = re.sub(r"^\.+|\.+$", "", springs)
        ## Collapse sections of operational springs
        springs = re.sub(r"\.{2,}", ".", springs)
        ## Split springs into sections
        springs = springs.split(".")
        # print("Type: .")
        # print(springs, groups)

        # Allocate groups and calculate arrangements
        group_combinations = split_groups(groups, len(springs) - 1)
        for group_combination in group_combinations:  # Consider possible cases
            case_arrangements = 1
            try:  # Valid case
                # Quick validity check prior to any calculation
                for springs_subset, groups_subset in zip(springs, group_combination):
                    assert (
                        len(springs_subset)
                        >= sum(groups_subset) + len(groups_subset) - 1
                    )
                    assert groups_subset != [] if "#" in springs_subset else True
                    assert springs_subset.count("#") <= sum(groups_subset)
                # Calculation
                # print("===== Case =====")
                for respective_subsets in zip(springs, group_combination):
                    case_arrangements *= get_arrangements(*respective_subsets)
                row_arrangements += case_arrangements
                # print(f"=== End Case === (Arrangements: {case_arrangements})")
            except AssertionError:  # Invalid case
                pass
        total_arrangements += row_arrangements
        # print("Arrangements:", row_arrangements)
    outputs.append(total_arrangements)
    # apparently simple brute force works for part 1, didn't rlly need the additional checks

    return outputs
