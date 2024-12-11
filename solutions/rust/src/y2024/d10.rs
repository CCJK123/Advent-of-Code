use std::{collections::HashSet, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .map(|s| {
            s.chars()
                .map(|c| c.to_digit(10).unwrap() as u8)
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    // Part 1
    let mut score = 0;
    let starting_coords_vec = input
        .iter()
        .enumerate()
        .map(|(i, row)| {
            row.iter()
                .enumerate()
                .filter(|(_, height)| **height == 0)
                .map(|(j, _)| [i, j])
                .collect::<Vec<_>>()
        })
        .reduce(|mut acc, e| {
            acc.extend(e);
            acc
        })
        .unwrap();
    for starting_coords in starting_coords_vec.iter() {
        let mut subsequent_coords = test_adjacent(&input, starting_coords, 1);
        for height in 2..10 {
            subsequent_coords = subsequent_coords
                .iter()
                .map(|coords| test_adjacent(&input, coords, height))
                .reduce(|mut acc, e| {
                    acc.extend(e);
                    acc
                })
                .unwrap();
        }
        score += subsequent_coords.len();
    }
    outputs.push(score);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn test_adjacent(input: &Vec<Vec<u8>>, coords: &[usize; 2], height: u8) -> HashSet<[usize; 2]> {
    let mut valid_adjacent_coords = Vec::new();
    if coords[0] > 0 {
        valid_adjacent_coords.push([coords[0] - 1, coords[1]])
    }
    if coords[1] > 0 {
        valid_adjacent_coords.push([coords[0], coords[1] - 1])
    }
    if coords[0] < input.len() - 1 {
        valid_adjacent_coords.push([coords[0] + 1, coords[1]])
    }
    if coords[1] < input[0].len() - 1 {
        valid_adjacent_coords.push([coords[0], coords[1] + 1])
    }
    valid_adjacent_coords
        .into_iter()
        .filter(|[i, j]| input[*i][*j] == height)
        .collect::<HashSet<_>>()
}
