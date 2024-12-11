use std::{collections::HashMap, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .split(" ")
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>();

    // Part 1 & 2 combined
    let mut stones = input.iter().fold(HashMap::new(), |mut acc, &s| {
        *acc.entry(s).or_insert(0) += 1;
        acc
    });
    let mut transformations = HashMap::<u64, Vec<u64>>::from([(0, vec![1])]);
    for blink_no in 0..75 {
        let mut stones_next = HashMap::new();
        for (stone, count) in stones.iter() {
            if !transformations.contains_key(stone) {
                transformations.insert(*stone, {
                    if stone.checked_ilog10().unwrap_or(0) % 2 == 1 {
                        let stone_string = stone.to_string();
                        let (left, right) = stone_string.split_at(
                            ((stone.checked_ilog10().unwrap() + 1) / 2)
                                .try_into()
                                .unwrap(),
                        );
                        vec![left.parse::<u64>().unwrap(), right.parse::<u64>().unwrap()]
                    } else {
                        vec![stone * 2024]
                    }
                });
            }
            for &child_stone in transformations[stone].iter() {
                *stones_next.entry(child_stone).or_insert(0) += count;
            }
        }
        stones = stones_next;
        // Part 1
        if blink_no == 24 {
            outputs.push(stones.values().sum::<u64>());
        }
    }
    outputs.push(stones.values().sum()); // Part 2

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
