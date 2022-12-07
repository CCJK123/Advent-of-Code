def day_07(input_str):
    # Initial setup
    input_array = [i.split("\n") for i in input_str.split("\n$ ")]
    input_array[0][0] = input_array[0][0][2:]
    outputs = []

    '''
    # Notes
    - Input seems to utilise breadth first search to find all directories
        - ~~Might need to have a stack of unsearched directories~~
        - Nevermind, not needed if I do the summations everytime a branch is fully explored
    - Can probably assume all directory names are unique
        - ~~Prob don't need to deal with storing entire paths, but might be better for clarity~~
        - Nevermind, wasn't unique, ended up having to debug due to that
    - File names irrelevant
    '''

    # Part 1
    unchecked_directories = []
    directory_sizes = {}
    current_directory_path = []

    # # Process all commands run
    for command in input_array:
        # Path management
        if command[0][:2] == "cd":
            if command[0][3:] == "..":
                # Sum sizes
                for size in directory_sizes["/".join(current_directory_path)].copy():
                    if type(size) == str:   # i.e. a temp directory pointer
                        directory_sizes["/".join(current_directory_path)
                                        ].remove(size)
                        directory_sizes["/".join(current_directory_path)
                                        ].append(directory_sizes["/".join(current_directory_path.copy() + [size])])
                directory_sizes["/".join(current_directory_path)
                                ] = sum(directory_sizes["/".join(current_directory_path)])
                # Move up a directory
                current_directory_path.pop()
            else:
                # Change to that directory
                current_directory_path.append(command[0][3:])

        # Directory size calculation
        elif command[0][:2] == "ls":
            directory_sizes["/".join(current_directory_path)] = []
            for element in command[1:]:
                if element[:3] == "dir":    # Add directory for now, replace w/ size later
                    directory_sizes["/".join(current_directory_path)
                                    ].append(element[4:])
                else:
                    directory_sizes["/".join(current_directory_path)
                                    ].append(int(element.split(" ")[0]))

    # # Final directory size calculations
    while current_directory_path != []:
        # Sum sizes
        for size in directory_sizes["/".join(current_directory_path)].copy():
            if type(size) == str:   # i.e. a temp directory pointer
                directory_sizes["/".join(current_directory_path)
                                ].remove(size)
                directory_sizes["/".join(current_directory_path)
                                ].append(directory_sizes["/".join(current_directory_path.copy() + [size])])
        directory_sizes["/".join(current_directory_path)
                        ] = sum(directory_sizes["/".join(current_directory_path)])
        # Move up a directory
        current_directory_path.pop()

    # # Calculate output
    total_size = 0
    for size in directory_sizes.values():
        if size <= 100000:
            total_size += size
    outputs.append(total_size)

    # Part 2
    unused_space = 70000000 - directory_sizes["/"]
    directory_size_list = list(directory_sizes.values())
    directory_size_list.sort()
    for size in directory_size_list:
        if unused_space + size >= 30000000:
            outputs.append(size)
            break

    return outputs
