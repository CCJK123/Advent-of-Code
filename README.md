# Advent of Code

This repository contains my (definitely not scuff) solutions to the annual Advent of Code (AoC) puzzles, which can be found [here](https://adventofcode.com).

## Getting Started

In line with the [wishes](https://adventofcode.com/2024/about#Can%20I%20copy/redistribute%20part%20of%20Advent%20of%20Code?:~:text=Can%20I%20copy,it%20something%20similar.) of AoC's creator, my puzzle inputs are not included in this repository, instead they are stored in a separate private repository and accessed via Git submodules. To run my solutions with your puzzle inputs, do the following:

1. Create a private Git repository on a service such as GitHub or GitLab, and populate it with your puzzle inputs. The puzzle input for a given year and day should be located at `<year>/<day>.txt`, where `<year>` is a 4 digit number and `<day>` is a 2 digit number (add zero padding for days 1 to 9). An example directory structure is shown below:

```
├ 2023
│ ├ 01.txt
│ ├ 02.txt
│ └ 03.txt
└ 2024
  ├ 23.txt
  ├ 24.txt
  └ 25.txt
```

2. Clone this git repository:

```sh
git clone https://github.com/CCJK123/Advent-of-Code
```

3. Modify `.gitmodules` to contain the remote URL to the Git repository you just created. Its file content should look similar to the following:

```gitmodules
[submodule "inputs"]
	path = inputs
	url = <your_repository_url_here>
```

4. Fetch puzzle input files from your private Git repository:

```sh
git submodule init
git submodule update
```
