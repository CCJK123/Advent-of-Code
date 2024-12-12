use std::{
    collections::{HashMap, HashSet},
    error::Error,
};

use itertools::Itertools;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .map(|s| s.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    // Part 1
    let mut antennas = HashMap::new();
    let mut antinode_coords = HashSet::new();
    for (i, row) in input.iter().enumerate() {
        for (j, &col) in row.iter().enumerate() {
            if col != '.' {
                antennas.entry(col).or_insert(HashSet::new()).insert([i, j]);
            }
        }
    }
    for same_frequency_antenna_coords in antennas.values() {
        for (&antenna_1, &antenna_2) in same_frequency_antenna_coords.iter().tuple_combinations() {
            antinode_coords.extend(get_antinodes(
                [antenna_1, antenna_2],
                [input.len() - 1, input[0].len() - 1],
            ));
        }
    }
    outputs.push(antinode_coords.len());

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn get_antinodes(antenna_pair_coords: [[usize; 2]; 2], max_coords: [usize; 2]) -> Vec<[usize; 2]> {
    let difference = [
        antenna_pair_coords[1][0] as i32 - antenna_pair_coords[0][0] as i32,
        antenna_pair_coords[1][1] as i32 - antenna_pair_coords[0][1] as i32,
    ];
    vec![
        [
            antenna_pair_coords[1][0] as i32 + difference[0],
            antenna_pair_coords[1][1] as i32 + difference[1],
        ],
        [
            antenna_pair_coords[0][0] as i32 - difference[0],
            antenna_pair_coords[0][1] as i32 - difference[1],
        ],
    ]
    .into_iter()
    .filter(|[x, y]| *x >= 0 && *x <= max_coords[0] as i32 && *y >= 0 && *y <= max_coords[1] as i32)
    .map(|[x, y]| [x as usize, y as usize])
    .collect()
}
