use itertools::Itertools;
use std::{cmp::Ordering, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .map(|s| {
            let mut line = s[2..].split(" v=").map(|s| {
                let mut coords = s.split(",").map(|s| s.parse::<i32>().unwrap());
                [coords.next().unwrap(), coords.next().unwrap()]
            });
            [line.next().unwrap(), line.next().unwrap()]
        })
        .collect::<Vec<_>>();
    let grid_size = [101, 103];

    // Part 1
    outputs.push(get_safety_factor(&input, 100, grid_size));

    // Part 2
    let mut seconds = 0;
    loop {
        seconds += 1;
        let robots = get_end_coords(&input, seconds, grid_size);
        let mut picture = vec![vec!['.'; grid_size[0] as usize]; grid_size[1] as usize];
        for robot in robots {
            picture[robot[1] as usize][robot[0] as usize] = '#';
        }
        if picture
            .iter()
            .map(|r| r.iter().collect::<String>())
            .any(|r| {
                r.contains("###############################") // Bodge
            })
        {
            let picture = picture
                .iter()
                .map(|r| r.iter().collect::<String>())
                .join("\n");
            println!("{picture}");
            break;
        }
    }
    outputs.push(seconds);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn get_end_coords(input: &Vec<[[i32; 2]; 2]>, seconds: i32, grid_size: [i32; 2]) -> Vec<[i32; 2]> {
    input
        .into_iter()
        .map(|[position, velocity]| {
            [
                (position[0] + velocity[0] * seconds).rem_euclid(grid_size[0]),
                (position[1] + velocity[1] * seconds).rem_euclid(grid_size[1]),
            ]
        })
        .collect()
}

fn get_safety_factor(input: &Vec<[[i32; 2]; 2]>, seconds: i32, grid_size: [i32; 2]) -> i32 {
    let robots = get_end_coords(input, seconds, grid_size);
    let mut quadrants = [0; 4];
    for robot in robots {
        match [
            robot[0].cmp(&(grid_size[0] / 2)),
            robot[1].cmp(&(grid_size[1] / 2)),
        ] {
            [Ordering::Greater, Ordering::Greater] => {
                quadrants[0] += 1;
            }
            [Ordering::Greater, Ordering::Less] => {
                quadrants[1] += 1;
            }
            [Ordering::Less, Ordering::Greater] => {
                quadrants[2] += 1;
            }
            [Ordering::Less, Ordering::Less] => {
                quadrants[3] += 1;
            }
            _ => {}
        }
    }
    quadrants.into_iter().reduce(|acc, c| acc * c).unwrap()
}
