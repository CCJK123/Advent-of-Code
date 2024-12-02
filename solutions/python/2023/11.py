def run(input_str):
    # Initial setup
    input_array = input_str.split("\n")
    outputs = []

    # Part 1
    image = input_array.copy()

    ## Account for "cosmic expansion"
    offset = 0
    for row_no, row in enumerate(input_array):
        if row == len(input_array[0]) * ".":
            image.insert(row_no + (offset := offset + 1), row)
    offset = 0
    for col_no in range(len(input_array[0])):
        if all([row[col_no] == "." for row in input_array]):
            for row_no, row in enumerate(image.copy()):
                image[row_no] = row[: col_no + offset] + "." + row[col_no + offset :]
            offset += 1

    ## Find all galaxies & get manhattan distance sum for all pairs
    galaxies_coords = [
        (row_no, col_no)
        for row_no, row in enumerate(image)
        for col_no, col in enumerate(row)
        if col == "#"
    ]
    length_sum = 0
    for galaxy_no_offset, galaxy_coords_1 in enumerate(galaxies_coords, start=1):
        for galaxy_coords_2 in galaxies_coords[galaxy_no_offset:]:
            length_sum += abs(galaxy_coords_1[0] - galaxy_coords_2[0])
            length_sum += abs(galaxy_coords_1[1] - galaxy_coords_2[1])
    outputs.append(length_sum)

    # Part 2
    ## Get indices of empty rows/cols in original image
    empty_indices = {"row": set(), "col": set()}
    for row_no, row in enumerate(input_array):
        if row == len(input_array[0]) * ".":
            empty_indices["row"].add(row_no)
    for col_no in range(len(input_array[0])):
        if all([row[col_no] == "." for row in input_array]):
            empty_indices["col"].add(col_no)

    ## Calculate manhattan distance with adjusted distances
    galaxies_coords = [
        (row_no, col_no)
        for row_no, row in enumerate(input_array)
        for col_no, col in enumerate(row)
        if col == "#"
    ]
    length_sum, expansion_factor = 0, 1000000
    for galaxy_no_offset, galaxy_coords_1 in enumerate(galaxies_coords, start=1):
        for galaxy_coords_2 in galaxies_coords[galaxy_no_offset:]:
            for coord_index, empty_index_type in enumerate(("row", "col")):
                length_sum += abs(
                    galaxy_coords_1[coord_index] - galaxy_coords_2[coord_index]
                )
                length_sum += (expansion_factor - 1) * len(
                    empty_indices[empty_index_type].intersection(
                        range(
                            min(
                                galaxy_coords_1[coord_index],
                                galaxy_coords_2[coord_index],
                            )
                            + 1,
                            max(
                                galaxy_coords_1[coord_index],
                                galaxy_coords_2[coord_index],
                            ),
                        )
                    )
                )
    outputs.append(length_sum)

    return outputs
