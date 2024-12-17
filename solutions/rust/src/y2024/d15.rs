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

    // Part 1
    let walls = get_char_coords(&input, '#');
    let mut boxes = get_char_coords(&input, 'O');
    let mut robot = get_char_coords(&input, '@').into_iter().next().unwrap();
    for &(direction_char, step_count) in &moves {
        let direction = get_direction(direction_char);
        let wall = get_closest_linear_obstacles(&walls, direction_char, &robot)
            .next()
            .unwrap();
        if manhattan_distance(&robot, wall) == 1 {
            continue; // Wall directly blocking movement
        }
        let current_boxes = get_closest_linear_obstacles(&boxes, direction_char, &robot)
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

    // Part 2
    let walls = get_char_coords(&input, '#')
        .into_iter()
        .map(|[x, y]| [[x, y * 2], [x, y * 2 + 1]])
        .flatten()
        .collect::<HashSet<_>>();
    let mut boxes = get_char_coords(&input, 'O')
        .into_iter()
        .map(|[x, y]| [[x, y * 2], [x, y * 2 + 1]])
        .collect::<HashSet<_>>();
    let mut robot = get_char_coords(&input, '@')
        .into_iter()
        .map(|[x, y]| [x, y * 2])
        .next()
        .unwrap();
    for &(direction_char, step_count) in &moves {
        // Assert no overlapping boxes (was for debugging)
        assert!(boxes.iter().all(|&[l, r]| boxes
            .iter()
            .all(|&b| { b == [l, r] || b.iter().all(|&s| s != l && s != r) })));

        let direction = get_direction(direction_char);
        let wall = get_closest_linear_obstacles(&walls, direction_char, &robot)
            .next()
            .unwrap();
        if manhattan_distance(&robot, wall) == 1 {
            continue; // Wall directly blocking movement
        }
        let (box_changes, robot_step_count) =
            propagate_wide_box_movement(&robot, &walls, &boxes, direction_char, step_count);
        let old_robot = robot;
        robot = move_steps(&robot, direction, robot_step_count);
        boxes = boxes
            .into_iter()
            .map(|old_box| {
                let relevant_change = box_changes
                    .iter()
                    .filter(|&&(side, _, _)| {
                        side != old_robot && (old_box[0] == side || old_box[1] == side)
                    })
                    .next();
                if let Some(&(_, direction, step_count)) = relevant_change {
                    [
                        move_steps(&old_box[0], direction, step_count),
                        move_steps(&old_box[1], direction, step_count),
                    ]
                } else {
                    old_box
                }
            })
            .collect::<HashSet<_>>();
    }
    let mut gps_coord_sum = 0;
    for [[x, y], _] in &boxes {
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

fn get_direction(direction_char: char) -> [i32; 2] {
    match direction_char {
        '^' => [-1, 0],
        'v' => [1, 0],
        '<' => [0, -1],
        '>' => [0, 1],
        _ => panic!(),
    }
}

fn manhattan_distance(a: &[i32; 2], b: &[i32; 2]) -> u32 {
    a[0].abs_diff(b[0]) + a[1].abs_diff(b[1])
}

fn get_closest_linear_obstacles<'a>(
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

fn get_closest_wide_box<'a>(
    boxes: &'a HashSet<[[i32; 2]; 2]>,
    direction_char: char,
    robot: &[i32; 2],
) -> Option<&'a [[i32; 2]; 2]> {
    boxes
        .iter()
        .filter(|b| match direction_char {
            '^' => b
                .iter()
                .any(|side| side[0] < robot[0] && side[1] == robot[1]),
            'v' => b
                .iter()
                .any(|side| side[0] > robot[0] && side[1] == robot[1]),
            '<' => b[0][0] == robot[0] && b[0][1] < robot[1],
            '>' => b[0][0] == robot[0] && b[0][1] > robot[1],
            _ => panic!(),
        })
        .sorted_by_key(|b| manhattan_distance(&b[0], robot).min(manhattan_distance(&b[1], robot)))
        .next()
}

fn propagate_wide_box_movement(
    reference: &[i32; 2],
    walls: &HashSet<[i32; 2]>,
    boxes: &HashSet<[[i32; 2]; 2]>,
    direction_char: char,
    max_step_count: u32,
) -> (HashSet<([i32; 2], [i32; 2], u32)>, u32) {
    let direction = get_direction(direction_char);
    let wall = get_closest_linear_obstacles(walls, direction_char, reference)
        .next()
        .unwrap();
    match get_closest_wide_box(&boxes, direction_char, reference) {
        None => {
            let step_count = max_step_count.min(manhattan_distance(reference, wall) - 1);
            (
                HashSet::from([(*reference, direction, step_count)]),
                step_count,
            )
        }
        Some(closest_box) => {
            // Handle cases where wall between box and reference
            // OR reference cannot reach closest box
            let distance_to_closest_box = manhattan_distance(&closest_box[0], reference)
                .min(manhattan_distance(&closest_box[1], reference));
            if manhattan_distance(wall, reference) < distance_to_closest_box
                || max_step_count < distance_to_closest_box
            {
                let step_count = max_step_count.min(manhattan_distance(reference, wall) - 1);
                return (
                    HashSet::from([(*reference, direction, step_count)]),
                    step_count,
                );
            }

            match direction_char {
                '^' | 'v' => {
                    let base_step_count = max_step_count
                        .min(manhattan_distance(&closest_box[0], reference) - 1)
                        .min(manhattan_distance(&closest_box[1], reference) - 1);
                    let [left, right] = closest_box;
                    let side_step_count = max_step_count - base_step_count;
                    let (mut left_box_changes, left_step_count) = propagate_wide_box_movement(
                        left,
                        walls,
                        boxes,
                        direction_char,
                        side_step_count,
                    );
                    let (mut right_box_changes, right_step_count) = propagate_wide_box_movement(
                        right,
                        walls,
                        boxes,
                        direction_char,
                        side_step_count,
                    );
                    // Move the maximum amount possible that both sides can move
                    if left_step_count > right_step_count {
                        (left_box_changes, _) = propagate_wide_box_movement(
                            left,
                            walls,
                            boxes,
                            direction_char,
                            right_step_count,
                        );
                    } else if right_step_count > left_step_count {
                        (right_box_changes, _) = propagate_wide_box_movement(
                            right,
                            walls,
                            boxes,
                            direction_char,
                            left_step_count,
                        );
                    }
                    let step_count = base_step_count + left_step_count.min(right_step_count);
                    let mut box_changes =
                        left_box_changes.union(&right_box_changes).map(|b| *b).fold(
                            HashSet::<([i32; 2], [i32; 2], u32)>::new(),
                            |mut acc, (side, dir, new_step)| {
                                let similar_change = acc
                                    .iter()
                                    .filter(|&&(s, d, _)| s == side && d == dir)
                                    .next();
                                match similar_change {
                                    Some(&(_, _, old_step)) => {
                                        // Ensure each box moves as far as possible
                                        // (different side branches can move later boxes different amounts)
                                        // (e.g. if only one side has air gaps between current box and later box)
                                        if new_step > old_step {
                                            acc.remove(&(side, dir, old_step));
                                            acc.insert((side, dir, new_step));
                                        }
                                    }
                                    None => {
                                        acc.insert((side, dir, new_step));
                                    }
                                }
                                acc
                            },
                        );
                    box_changes.insert((*reference, direction, step_count));
                    (box_changes, step_count)
                }
                '<' | '>' => {
                    let [close, far] = if direction_char == '<' {
                        [closest_box[1], closest_box[0]]
                    } else {
                        *closest_box
                    };
                    let base_step_count =
                        max_step_count.min(manhattan_distance(&close, reference) - 1);
                    let (mut box_changes, additional_step_count) = propagate_wide_box_movement(
                        &far,
                        walls,
                        boxes,
                        direction_char,
                        max_step_count - base_step_count,
                    );
                    let step_count = base_step_count + additional_step_count;
                    box_changes.insert((*reference, direction, step_count));
                    (box_changes, step_count)
                }
                _ => panic!(),
            }
        }
    }
}
