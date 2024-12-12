use itertools::Itertools;
use std::{collections::HashSet, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .map(|s| s.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    // Part 1
    // println!("Input: {input:?}");
    let mut price = 0;
    let mut unchecked = (0..input.len())
        .cartesian_product(0..input[0].len())
        .map(|(x, y)| [x, y])
        .collect::<HashSet<_>>();
    // println!("{unchecked:?}");
    while unchecked.len() != 0 {
        let mut area = 0;
        let mut perimeter = 0;

        let starting_plant_coords = unchecked.iter().next().unwrap().clone();
        let plant_type = input[starting_plant_coords[0]][starting_plant_coords[1]];
        let mut plants_pending_checking = HashSet::from([starting_plant_coords]);
        while plants_pending_checking.len() != 0 {
            let current_plant_coords = plants_pending_checking.iter().next().unwrap().clone();
            plants_pending_checking.remove(&current_plant_coords);
            area += 1;
            let subsequent_plant_coords =
                get_similar_adjacent_plants(plant_type, current_plant_coords, &input);
            perimeter += 4 - subsequent_plant_coords.len();
            plants_pending_checking.extend(
                subsequent_plant_coords
                    .into_iter()
                    .filter(|coords| unchecked.contains(coords)),
            );
            unchecked.remove(&current_plant_coords);
        }

        price += area * perimeter;
    }
    outputs.push(price);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn get_similar_adjacent_plants(
    plant_type: char,
    coords: [usize; 2],
    input: &Vec<Vec<char>>,
) -> Vec<[usize; 2]> {
    let mut adjacent_coords = Vec::new();
    if coords[0] > 0 {
        adjacent_coords.push([coords[0] - 1, coords[1]]);
    }
    if coords[1] > 0 {
        adjacent_coords.push([coords[0], coords[1] - 1]);
    }
    if coords[0] < input.len() - 1 {
        adjacent_coords.push([coords[0] + 1, coords[1]])
    }
    if coords[1] < input[0].len() - 1 {
        adjacent_coords.push([coords[0], coords[1] + 1])
    }
    adjacent_coords
        .into_iter()
        .filter(|[x, y]| input[*x][*y] == plant_type)
        .collect()
}
