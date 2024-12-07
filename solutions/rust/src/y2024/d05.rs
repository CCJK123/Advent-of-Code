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
    let mut incorrect_updates = Vec::new(); // Part 2
    for rule in input.0.iter() {
        let (before, after) = (rule[0], rule[1]);
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
        } else {
            // Part 2
            incorrect_updates.push(update);
        }
    }
    outputs.push(score);

    // Part 2
    let mut score = 0;
    for update in incorrect_updates {
        let mut new_update = Vec::new();
        let rules = input
            .0
            .iter()
            .filter(|r| r.into_iter().all(|p| update.contains(p)))
            .collect::<Vec<_>>();
        for _ in 0..update.len() {
            let next_page_options = update
                .iter()
                .filter(|p| {
                    !new_update.contains(p)
                        && rules
                            .iter()
                            .filter(|r| **p == r[1])
                            .all(|r| new_update.contains(&&r[0]))
                })
                .collect::<Vec<_>>();
            assert_eq!(next_page_options.len(), 1);
            new_update.push(next_page_options[0]);
        }
        score += new_update[(new_update.len() - 1) / 2]
            .parse::<u32>()
            .unwrap();
    }
    outputs.push(score);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
