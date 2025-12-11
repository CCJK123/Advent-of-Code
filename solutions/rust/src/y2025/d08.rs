use std::error::Error;

use itertools::Itertools;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let boxes = input
        .lines()
        .map(|s| {
            let mut v = s.split(",").map(|x| x.parse::<u64>().unwrap());
            [v.next().unwrap(), v.next().unwrap(), v.next().unwrap()]
        })
        .collect_vec();
    let sorted_box_pairs = boxes
        .iter()
        .combinations(2)
        .map(|v| {
            (
                [v[0], v[1]],
                (0..=2)
                    .map(|i| v[0][i].abs_diff(v[1][i]).pow(2))
                    .sum::<u64>(),
            )
        })
        .sorted_by(|a, b| Ord::cmp(&a.1, &b.1))
        .map(|(pair, _squared_distance)| pair)
        .collect_vec();

    // Part 1
    let mut circuits = boxes.iter().map(|b| vec![b]).collect_vec();
    for [box_1, box_2] in sorted_box_pairs.iter().take(1000) {
        let box_1_index = circuits
            .iter()
            .position(|boxes| boxes.contains(box_1))
            .unwrap();
        let box_2_index = circuits
            .iter()
            .position(|boxes| boxes.contains(box_2))
            .unwrap();

        if box_1_index == box_2_index {
            continue;
        }
        let other = circuits[box_2_index].clone();
        circuits[box_1_index].extend(other);
        circuits.remove(box_2_index);
    }

    let circuit_sizes = circuits.iter().map(|boxes| boxes.len()).sorted().rev();
    let score = circuit_sizes.take(3).product::<usize>();
    outputs.push(score as u64);

    // Part 2
    let mut circuits = boxes.iter().map(|b| vec![b]).collect_vec();
    let mut score = 0;
    for [box_1, box_2] in sorted_box_pairs.iter() {
        let box_1_index = circuits
            .iter()
            .position(|boxes| boxes.contains(box_1))
            .unwrap();
        let box_2_index = circuits
            .iter()
            .position(|boxes| boxes.contains(box_2))
            .unwrap();

        if box_1_index == box_2_index {
            continue;
        }
        let other = circuits[box_2_index].clone();
        circuits[box_1_index].extend(other);
        circuits.remove(box_2_index);

        if circuits.len() == 1 {
            score = box_1[0] * box_2[0];
            break;
        }
    }
    outputs.push(score);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
