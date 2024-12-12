use itertools::Itertools;
use std::{cmp::Ordering, collections::HashSet, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .map(|s| s.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    // Part 1 and 2 combined
    let mut price = 0; // Part 1
    let mut discounted_price = 0; // Part 2
    let mut unchecked = (0..input.len())
        .cartesian_product(0..input[0].len())
        .map(|(x, y)| [x, y])
        .collect::<HashSet<_>>();
    while unchecked.len() != 0 {
        let mut area = 0;
        let mut perimeter = 0; // Part 1
        let mut side_segments = HashSet::new(); // Part 2

        let starting_plant_coords = unchecked.iter().next().unwrap().clone();
        let plant_type = input[starting_plant_coords[0]][starting_plant_coords[1]];
        let mut plants_pending_checking = HashSet::from([starting_plant_coords]);
        while plants_pending_checking.len() != 0 {
            let current_plant_coords = plants_pending_checking.iter().next().unwrap().clone();
            plants_pending_checking.remove(&current_plant_coords);
            area += 1;

            // Part 1
            let subsequent_plant_coords =
                get_similar_adjacent_plants(plant_type, current_plant_coords, &input);
            perimeter += 4 - subsequent_plant_coords.len();
            // Part 2
            side_segments.extend(get_side_segments(plant_type, current_plant_coords, &input));

            plants_pending_checking.extend(
                subsequent_plant_coords
                    .into_iter()
                    .filter(|coords| unchecked.contains(coords)),
            );
            unchecked.remove(&current_plant_coords);
        }

        // Part 1
        price += area * perimeter;
        // Part 2
        let mut sides = 0;
        let mut current_side_segments = HashSet::new();
        while side_segments.len() != 0 {
            let mut next_side_segments = side_segments
                .iter()
                .filter(|seg| {
                    current_side_segments
                        .iter()
                        .any(|current_seg: &[[usize; 2]; 2]| {
                            match [
                                current_seg[0][0].cmp(&current_seg[1][0]),
                                current_seg[0][1].cmp(&current_seg[1][1]),
                            ] {
                                [Ordering::Greater | Ordering::Less, Ordering::Equal] => {
                                    // Segment is horizontal
                                    itertools::concat([
                                        vec![[
                                            [current_seg[0][0], current_seg[0][1] + 1],
                                            [current_seg[1][0], current_seg[1][1] + 1],
                                        ]],
                                        {
                                            if current_seg[0][1] > 0 && current_seg[1][1] > 0 {
                                                vec![[
                                                    [current_seg[0][0], current_seg[0][1] - 1],
                                                    [current_seg[1][0], current_seg[1][1] - 1],
                                                ]]
                                            } else {
                                                Vec::new()
                                            }
                                        },
                                    ])
                                }
                                [Ordering::Equal, Ordering::Greater | Ordering::Less] => {
                                    // Segment is vertical
                                    itertools::concat([
                                        vec![[
                                            [current_seg[0][0] + 1, current_seg[0][1]],
                                            [current_seg[1][0] + 1, current_seg[1][1]],
                                        ]],
                                        {
                                            if current_seg[0][0] > 0 && current_seg[1][0] > 0 {
                                                vec![[
                                                    [current_seg[0][0] - 1, current_seg[0][1]],
                                                    [current_seg[1][0] - 1, current_seg[1][1]],
                                                ]]
                                            } else {
                                                Vec::new()
                                            }
                                        },
                                    ])
                                }
                                _ => panic!(),
                            }
                            .contains(seg)
                        })
                })
                .map(|s| *s)
                .collect::<HashSet<_>>();
            if next_side_segments.len() == 0 {
                next_side_segments.insert(side_segments.iter().next().unwrap().clone());
                current_side_segments = HashSet::new();
                sides += 1;
            }
            current_side_segments.extend(&next_side_segments);
            for side_segment in &next_side_segments {
                side_segments.remove(side_segment);
            }
        }
        discounted_price += area * sides;
    }
    outputs.extend([price, discounted_price]);

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

fn get_side_segments(
    plant_type: char,
    coords: [usize; 2],
    input: &Vec<Vec<char>>,
) -> Vec<[[usize; 2]; 2]> {
    let coords = [coords[0] + 1, coords[1] + 1];
    vec![
        [coords[0] - 1, coords[1]],
        [coords[0], coords[1] - 1],
        [coords[0] + 1, coords[1]],
        [coords[0], coords[1] + 1],
    ]
    .into_iter()
    .filter(|[x, y]| {
        *x == 0
            || *y == 0
            || *x == input.len() + 1
            || *y == input[0].len() + 1
            || input[*x - 1][*y - 1] != plant_type
    })
    .map(|c| [coords, c])
    .collect()
}
