use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let homework = input
        .lines()
        .map(|s| s.split_whitespace().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    // Part 1
    let total = (0..homework[0].len())
        .map(|i| match homework[homework.len() - 1][i] {
            "+" => (0..=(homework.len() - 2))
                .map(|j| homework[j][i].parse::<u64>().unwrap())
                .sum::<u64>(),
            "*" => (0..=(homework.len() - 2))
                .map(|j| homework[j][i].parse::<u64>().unwrap())
                .product::<u64>(),
            a => panic!("{a}"),
        })
        .sum::<u64>();
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
