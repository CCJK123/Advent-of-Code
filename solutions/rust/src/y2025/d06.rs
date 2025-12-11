use std::error::Error;

use itertools::Itertools;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    let homework = input
        .lines()
        .map(|s| s.split_whitespace().collect::<Vec<_>>())
        .collect::<Vec<_>>();
    let total = (0..homework[0].len())
        .map(|i| {
            let numbers =
                (0..=(homework.len() - 2)).map(|j| homework[j][i].parse::<u64>().unwrap());
            match homework[homework.len() - 1][i] {
                "+" => numbers.sum::<u64>(),
                "*" => numbers.product::<u64>(),
                _ => panic!(),
            }
        })
        .sum::<u64>();
    outputs.push(total);

    // Part 2
    let homework = input
        .lines()
        .map(|s| {
            let mut v = s.chars().collect::<Vec<_>>();
            v.insert(0, ' ');
            v
        })
        .collect::<Vec<_>>();
    let mut problems = vec![];
    for i in 0..homework[0].len() {
        if ['+', '*'].contains(&homework[homework.len() - 1][i]) {
            problems.push((homework[homework.len() - 1][i], vec![]));
        }

        let number = match (0..(homework.len() - 1))
            .map(|j| homework[j][i])
            .join("")
            .trim()
            .parse::<u64>()
        {
            Err(_) => continue,
            Ok(x) => x,
        };
        let problem_count = problems.len();
        problems[problem_count - 1].1.push(number);
    }

    let total = problems
        .iter()
        .map(|(operator, numbers)| match operator {
            '+' => numbers.iter().sum::<u64>(),
            '*' => numbers.iter().product::<u64>(),
            _ => panic!(),
        })
        .sum::<u64>();
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
