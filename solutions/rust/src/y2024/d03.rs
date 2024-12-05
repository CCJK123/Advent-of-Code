use regex::Regex;
use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    outputs.push(get_mul_total(input));

    // Part 2
    let mut total = 0;
    for capture in Regex::new(r"(?s)do\(\).*?don't\(\)")
        .unwrap()
        .captures_iter(&format!("do(){input}don't()"))
    {
        total += get_mul_total(capture.get(0).unwrap().as_str());
    }
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn get_mul_total(haystack: &str) -> u32 {
    let mut total = 0;
    for (_, [no_1, no_2]) in Regex::new(r"mul\((\d+),(\d+)\)")
        .unwrap()
        .captures_iter(haystack)
        .map(|c| c.extract())
    {
        total += no_1.parse::<u32>().unwrap() * no_2.parse::<u32>().unwrap();
    }
    total
}
