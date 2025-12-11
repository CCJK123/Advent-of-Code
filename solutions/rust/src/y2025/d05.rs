use std::error::Error;

use itertools::Itertools;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let mut database = input.lines();
    let fresh_ingredient_id_ranges = database
        .by_ref()
        .take_while(|s| *s != "")
        .map(|s| {
            let mut range = s.split("-").map(|s| s.parse::<u64>().unwrap());
            range.next().unwrap()..=range.next().unwrap()
        })
        .collect::<Vec<_>>();
    let available_ingredient_ids = database
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>();

    // Part 1
    let count = available_ingredient_ids
        .iter()
        .map(|ingredient_id| {
            fresh_ingredient_id_ranges
                .iter()
                .any(|range| range.contains(ingredient_id)) as u64
        })
        .sum::<u64>();
    outputs.push(count);

    // Part 2
    let mut current_ranges = fresh_ingredient_id_ranges.clone();
    loop {
        let mut old_ranges = vec![];
        for (i, range_1) in current_ranges.iter().enumerate() {
            for range_2 in &current_ranges[(i + 1)..] {
                if range_1.contains(range_2.start())
                    || range_1.contains(range_2.end())
                    || (
                        // If range 2 is a superset of range 1
                        range_2.contains(range_1.start())
                    )
                {
                    old_ranges.push(range_1.clone());
                    old_ranges.push(range_2.clone());
                    break;
                }
            }
            if old_ranges.len() != 0 {
                break;
            }
        }
        if old_ranges.len() != 0 {
            let range_1 = &old_ranges[0];
            let range_2 = &old_ranges[1];
            current_ranges.retain(|range| range != range_1 && range != range_2);
            current_ranges
                .push(*range_1.start().min(range_2.start())..=*range_1.end().max(range_2.end()));
            continue;
        }
        break;
    }
    let count = current_ranges
        .iter()
        .map(|range| range.try_len().unwrap() as u64)
        .sum::<u64>();
    outputs.push(count);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
