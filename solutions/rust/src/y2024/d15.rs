use itertools::Itertools;
use std::{collections::HashSet, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input.lines().fold(vec![Vec::new()], |mut acc, s| {
        if s.len() == 0 {
            acc.push(Vec::new());
        } else {
            let index = acc.len() - 1;
            acc[index].push(s);
        }
        acc
    });
    let input = (
        input[0]
            .iter()
            .map(|s| s.chars().collect::<Vec<_>>())
            .collect::<Vec<_>>(),
        input[1].join(""),
    );

    // Part 1
    let walls = get_char_coords(&input, '#');
    let mut boxes = get_char_coords(&input, 'O');
    let mut robot = get_char_coords(&input, '@').into_iter().next().unwrap();
    let moves = input
        .1
        .chars()
        .fold(Vec::<(char, u32)>::new(), |mut acc, c| {
            if acc.len() == 0 || acc[acc.len() - 1].0 != c {
                acc.push((c, 1));
            } else {
                let index = acc.len() - 1;
                acc[index].1 += 1;
            }
            acc
        });
    for (direction_char, step_count) in moves {
        let direction = match direction_char {
            '^' => [-1, 0],
            'v' => [1, 0],
            '<' => [0, -1],
            '>' => [0, 1],
            _ => panic!(),
        };
        let wall = get_closest_linear_obstacle(&walls, direction_char, &robot)
            .next()
            .unwrap();
        if manhattan_distance(&robot, wall) == 1 {
            continue; // Wall directly blocking movement
        }
        let current_boxes = get_closest_linear_obstacle(&boxes, direction_char, &robot)
            .filter(|&&b| robot.min(*wall) < b && b < robot.max(*wall))
            .rev()
            .collect::<Vec<_>>();
        let (mut moved_boxes, _) =
            propagate_movement(&robot, wall, current_boxes.clone(), direction, step_count);
        robot = moved_boxes.pop().unwrap();
        for (old_box, new_box) in current_boxes
            .into_iter()
            .map(|b| *b)
            .zip(moved_boxes.into_iter())
            .collect::<Vec<_>>()
        {
            if old_box != new_box {
                boxes.remove(&old_box);
                boxes.insert(new_box);
            }
        }
    }

    let mut gps_coord_sum = 0;
    for [x, y] in &boxes {
        gps_coord_sum += 100 * x + y
    }
    outputs.push(gps_coord_sum);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn get_char_coords(input: &(Vec<Vec<char>>, String), character: char) -> HashSet<[i32; 2]> {
    input
        .0
        .iter()
        .enumerate()
        .map(|(i, v)| {
            v.iter()
                .enumerate()
                .fold(HashSet::new(), |mut acc, (j, c)| {
                    if *c == character {
                        acc.insert([i as i32, j as i32]);
                    }
                    acc
                })
        })
        .flatten()
        .collect()
}

fn manhattan_distance(a: &[i32; 2], b: &[i32; 2]) -> u32 {
    a[0].abs_diff(b[0]) + a[1].abs_diff(b[1])
}

fn get_closest_linear_obstacle<'a>(
    obstacles: &'a HashSet<[i32; 2]>,
    direction_char: char,
    robot: &[i32; 2],
) -> std::vec::IntoIter<&'a [i32; 2]> {
    obstacles
        .iter()
        .filter(|obstacle| match direction_char {
            '^' => obstacle[0] < robot[0] && obstacle[1] == robot[1],
            'v' => obstacle[0] > robot[0] && obstacle[1] == robot[1],
            '<' => obstacle[0] == robot[0] && obstacle[1] < robot[1],
            '>' => obstacle[0] == robot[0] && obstacle[1] > robot[1],
            _ => panic!(),
        })
        .sorted_by_key(|obstacle| manhattan_distance(obstacle, robot))
}

fn move_steps(reference: &[i32; 2], direction: [i32; 2], step_count: u32) -> [i32; 2] {
    [
        reference[0] + step_count as i32 * direction[0],
        reference[1] + step_count as i32 * direction[1],
    ]
}

fn propagate_movement(
    reference: &[i32; 2],
    wall: &[i32; 2],
    mut boxes: Vec<&[i32; 2]>,
    direction: [i32; 2],
    max_step_count: u32,
) -> (Vec<[i32; 2]>, u32) {
    if boxes.len() == 0 {
        let step_count = max_step_count.min(manhattan_distance(reference, wall) - 1);
        return (
            vec![move_steps(reference, direction, step_count)],
            step_count,
        );
    }

    let next_box = boxes.pop().unwrap();
    let base_step_count = max_step_count.min(manhattan_distance(reference, next_box) - 1);
    let (mut moved_boxes, additional_step_count) = propagate_movement(
        next_box,
        wall,
        boxes,
        direction,
        max_step_count - base_step_count,
    );
    let step_count = base_step_count + additional_step_count;
    moved_boxes.push(move_steps(reference, direction, step_count));
    (moved_boxes, step_count)
}
