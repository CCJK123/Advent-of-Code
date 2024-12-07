use std::{
    collections::{HashMap, HashSet},
    error::Error,
};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input.lines().collect::<Vec<_>>();

    // Part 1
    let mut visted_coords = HashSet::<(isize, isize)>::new();
    let mut current_coords = input
        .iter()
        .enumerate()
        .filter_map(|(row_index, row)| match row.find("^") {
            Some(col_index) => Some((row_index as isize, col_index as isize)),
            None => None,
        })
        .collect::<Vec<_>>()[0];
    let mut direction: [isize; 2] = [-1, 0];
    let direction_map = HashMap::<[isize; 2], [isize; 2]>::from([
        ([-1, 0], [0, 1]),
        ([0, 1], [1, 0]),
        ([1, 0], [0, -1]),
        ([0, -1], [-1, 0]),
    ]);
    loop {
        visted_coords.insert(current_coords);
        let mut next_coords = (
            current_coords.0 + direction[0],
            current_coords.1 + direction[1],
        );
        if check_coords(&input, next_coords) {
            break;
        }
        // Adjust for obstruction
        if input[next_coords.0 as usize]
            .chars()
            .nth(next_coords.1 as usize)
            .unwrap()
            == '#'
        {
            direction = *direction_map.get(&direction).unwrap();
            next_coords = (
                current_coords.0 + direction[0],
                current_coords.1 + direction[1],
            );
            if check_coords(&input, next_coords) {
                break;
            }
        }
        // Move a step
        current_coords = next_coords;
    }
    outputs.push(visted_coords.len());

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn check_coords(input: &Vec<&str>, coords: (isize, isize)) -> bool {
    coords.0 < 0
        || coords.0 as usize >= input.len()
        || coords.1 < 0
        || coords.1 as usize >= input[0].len()
}
