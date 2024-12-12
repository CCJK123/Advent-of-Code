use std::{collections::HashMap, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .map(|s| s.split(": ").collect::<Vec<_>>())
        .map(|v| {
            (
                v[0].parse().unwrap(),
                v[1].split(" ").map(|s| s.parse().unwrap()).collect(),
            )
        })
        .collect::<HashMap<u64, Vec<u64>>>();

    // Part 1
    let mut total = 0;
    for (result, values) in &input {
        if values
            .iter()
            .fold(Vec::new(), |mut acc, &v| {
                if acc.len() == 0 {
                    acc.push(v);
                    acc
                } else {
                    acc.iter()
                        .map(|old| [old + v, old * v])
                        .flatten()
                        .collect::<Vec<_>>()
                }
            })
            .iter()
            .any(|v| v == result)
        {
            total += result;
        }
    }
    outputs.push(total);

    // Part 2
    let mut total = 0;
    for (result, values) in &input {
        if values
            .iter()
            .fold(Vec::new(), |mut acc, &v| {
                if acc.len() == 0 {
                    acc.push(v);
                    acc
                } else {
                    acc.iter()
                        .map(|old| [old + v, old * v, old * 10u64.pow(v.ilog10() + 1) + v])
                        .flatten()
                        .collect::<Vec<_>>()
                }
            })
            .iter()
            .any(|v| v == result)
        {
            total += result;
        }
    }
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
