use regex::Regex;
use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    let mut total = 0;
    for (_, [no_1, no_2]) in Regex::new(r"mul\((\d+),(\d+)\)")
        .unwrap()
        .captures_iter(input)
        .map(|c| c.extract())
    {
        total += no_1.parse::<u32>().unwrap() * no_2.parse::<u32>().unwrap();
    }
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
