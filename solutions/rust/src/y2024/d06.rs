use std::{
    collections::{HashMap, HashSet},
    error::Error,
};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input.lines().collect::<Vec<_>>();
    let starting_coords = input
        .iter()
        .enumerate()
        .filter_map(|(row_index, row)| match row.find("^") {
            Some(col_index) => Some([row_index as isize, col_index as isize]),
            None => None,
        })
        .collect::<Vec<_>>()[0];
    let direction_map = HashMap::<[isize; 2], [isize; 2]>::from([
        ([-1, 0], [0, 1]),
        ([0, 1], [1, 0]),
        ([1, 0], [0, -1]),
        ([0, -1], [-1, 0]),
    ]);

    // Part 1
    let mut visited_coords = HashSet::<[isize; 2]>::new();
    let mut current_coords = starting_coords;
    let mut direction: [isize; 2] = [-1, 0];
    loop {
        visited_coords.insert(current_coords);
        [current_coords, direction] =
            match get_next_step(&input, current_coords, direction, &direction_map) {
                Some(step) => step,
                None => break,
            };
    }
    outputs.push(visited_coords.len());

    // Part 2
    let mut count = 0;
    for obstruction_coords in
        (0..input.len()).flat_map(|r| (0..input[0].len()).map(move |c| [r, c]))
    {
        if input[obstruction_coords[0]]
            .chars()
            .nth(obstruction_coords[1])
            .unwrap()
            != '.'
        {
            continue;
        }
        let input = input
            .clone()
            .iter()
            .enumerate()
            .map(|(row_index, row)| {
                let mut col = String::from(*row);

                if row_index == obstruction_coords[0] {
                    col.replace_range(obstruction_coords[1]..obstruction_coords[1] + 1, "#");
                };
                col
            })
            .collect::<Vec<_>>();

        let mut traversed_paths = HashSet::<[[isize; 2]; 2]>::new();
        let mut current_coords = starting_coords;
        let mut direction: [isize; 2] = [-1, 0];
        loop {
            if traversed_paths.contains(&[current_coords, direction]) {
                count += 1;
                break;
            }
            traversed_paths.insert([current_coords, direction]);
            [current_coords, direction] =
                match get_next_step(&input, current_coords, direction, &direction_map) {
                    Some(step) => step,
                    None => break,
                };
        }
    }
    outputs.push(count);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn check_coords<T: AsRef<str>>(input: &Vec<T>, coords: [isize; 2]) -> bool {
    coords[0] < 0
        || coords[0] as usize >= input.len()
        || coords[1] < 0
        || coords[1] as usize >= input[0].as_ref().len()
}

fn get_next_step<T: AsRef<str>>(
    input: &Vec<T>,
    current_coords: [isize; 2],
    mut direction: [isize; 2],
    direction_map: &HashMap<[isize; 2], [isize; 2]>,
) -> Option<[[isize; 2]; 2]> {
    let mut next_coords = [
        current_coords[0] + direction[0],
        current_coords[1] + direction[1],
    ];
    if check_coords(&input, next_coords) {
        return None;
    }

    // Adjust for obstruction(s)
    if input[next_coords[0] as usize]
        .as_ref()
        .chars()
        .nth(next_coords[1] as usize)
        .unwrap()
        == '#'
    {
        // Obstruction exists, turn on the spot (to account for corner-forming obstructions)
        next_coords = current_coords;
        direction = *direction_map.get(&direction).unwrap();
    }

    Some([next_coords, direction])
}
