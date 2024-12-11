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

    // Parts 1 & 2 combined
    let mut score = 0; // Part 1
    let mut rating = 0; // Part 2
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
        let mut subsequent_coords_p2 = test_adjacent(&input, starting_coords, 1);
        let mut subsequent_coords_p1: HashSet<&[usize; 2]> =
            HashSet::from_iter(&subsequent_coords_p2);
        for height in 2..10 {
            subsequent_coords_p2 = subsequent_coords_p2
                .iter()
                .map(|coords| test_adjacent(&input, coords, height))
                .reduce(|mut acc, e| {
                    acc.extend(e);
                    acc
                })
                .unwrap();
            subsequent_coords_p1 = HashSet::from_iter(&subsequent_coords_p2);
        }
        score += subsequent_coords_p1.len();
        rating += subsequent_coords_p2.len();
    }
    outputs.push(score);
    outputs.push(rating);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn test_adjacent(input: &Vec<Vec<u8>>, coords: &[usize; 2], height: u8) -> Vec<[usize; 2]> {
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
        .collect::<Vec<_>>()
}
