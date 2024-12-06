use std::{collections::HashMap, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = (
        input
            .lines()
            .take_while(|s| s.len() != 0)
            .map(|s| s.split("|").collect::<Vec<_>>())
            .collect::<Vec<_>>(),
        input
            .lines()
            .skip_while(|s| s.len() != 0)
            .skip(1)
            .map(|s| s.split(",").collect::<Vec<_>>())
            .collect::<Vec<_>>(),
    );

    // Part 1
    let mut score = 0;
    let mut requirements = HashMap::new();
    for requirement in input.0.iter() {
        let (before, after) = (requirement[0], requirement[1]);
        if !requirements.contains_key(after) {
            requirements.insert(after, vec![before]);
        } else {
            requirements.get_mut(after).unwrap().push(before);
        }
    }
    for update in input.1.iter() {
        let mut is_correct = true;
        for (index, page) in update.iter().enumerate() {
            if requirements.contains_key(page)
                && requirements[page]
                    .iter()
                    .any(|p| update.contains(p) && !update[..index].contains(p))
            {
                is_correct = false
            }
        }
        if is_correct {
            score += update[(update.len() - 1) / 2].parse::<u32>().unwrap()
        }
    }
    outputs.push(score);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
