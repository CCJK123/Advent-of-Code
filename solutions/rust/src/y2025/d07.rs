use std::{collections::HashMap, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let layout = input
        .lines()
        .map(|s| s.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    // Part 1
    let mut count = 0;
    let mut beams = vec![layout[0].iter().position(|c| *c == 'S').unwrap()];
    for row in &layout[1..] {
        let mut new_beams = beams.clone();
        let splitter_indices = row
            .iter()
            .enumerate()
            .filter(|(_i, c)| **c == '^')
            .map(|(i, _c)| i);
        for splitter_index in splitter_indices {
            if beams.contains(&splitter_index) {
                new_beams.retain(|i| *i != splitter_index);
                new_beams.push(splitter_index - 1);
                new_beams.push(splitter_index + 1);
                count += 1;
            }
        }
        new_beams.dedup();
        beams = new_beams;
    }
    outputs.push(count);

    // Part 2
    let mut states = HashMap::<_, u64>::new();
    states.insert(layout[0].iter().position(|c| *c == 'S').unwrap(), 1);

    for row in &layout[1..] {
        let mut new_states = states.clone();
        let splitter_indices = row
            .iter()
            .enumerate()
            .filter(|(_i, c)| **c == '^')
            .map(|(i, _c)| i);
        for splitter_index in splitter_indices {
            if states.contains_key(&splitter_index) {
                new_states.remove(&splitter_index);
                *new_states.entry(splitter_index - 1).or_default() += states[&splitter_index];
                *new_states.entry(splitter_index + 1).or_default() += states[&splitter_index];
            }
        }
        states = new_states;
    }
    let count = states.values().sum();
    outputs.push(count);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
