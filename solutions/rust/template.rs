use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    println!("Input: {input}");

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
