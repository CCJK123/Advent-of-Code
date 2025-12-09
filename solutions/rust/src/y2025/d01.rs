use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let rotations = input
        .lines()
        .map(|rotation| match &rotation[0..1] {
            "L" => -rotation[1..].parse::<i16>().unwrap(),
            "R" => rotation[1..].parse::<i16>().unwrap(),
            _ => panic!(),
        })
        .collect::<Vec<_>>();

    // Part 1
    let mut count = 0;
    let mut dial_value = 50;
    for rotation in rotations.iter() {
        dial_value = (dial_value + rotation) % 100;
        if dial_value == 0 {
            count += 1;
        }
    }
    outputs.push(count);

    // Part 2
    count = 0;
    dial_value = 50;
    for rotation in rotations.iter() {
        let old_dial_value = dial_value;
        dial_value = dial_value + rotation;
        count += dial_value.abs() / 100;
        if old_dial_value != 0 && old_dial_value.signum() != dial_value.signum() {
            count += 1;
        }
        dial_value %= 100;
    }
    outputs.push(count);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
