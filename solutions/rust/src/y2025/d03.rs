use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let battery_banks = input
        .lines()
        .map(|bank| {
            bank.chars()
                .map(|c| c.to_digit(10).unwrap() as u64)
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    // Part 1
    let mut max_joltage = 0;
    for battery_bank in battery_banks.iter() {
        let digit_1 = battery_bank[..=(battery_bank.len() - 2)]
            .iter()
            .max()
            .unwrap();
        let digit_1_index = battery_bank[..=(battery_bank.len() - 2)]
            .iter()
            .position(|d| d == digit_1)
            .unwrap();

        let digit_2 = battery_bank[(digit_1_index + 1)..].iter().max().unwrap();

        max_joltage += digit_1 * 10 + digit_2;
    }
    outputs.push(max_joltage);

    // Part 2
    let battery_count = 12;
    let mut max_joltage = 0;
    for battery_bank in battery_banks.iter() {
        let mut digits = vec![];
        let mut available_batteries = battery_bank.clone();
        for i in 0..battery_count {
            let digit = *available_batteries[..=(available_batteries.len() + i - battery_count)]
                .iter()
                .max()
                .unwrap();
            let digit_index = available_batteries
                [..=(available_batteries.len() + i - battery_count)]
                .iter()
                .position(|d| d == &digit)
                .unwrap();

            digits.push(digit);
            available_batteries.drain(..=digit_index);
        }
        max_joltage += digits
            .iter()
            .rev()
            .enumerate()
            .map(|(i, d)| d * 10u64.pow(i as u32))
            .sum::<u64>();
    }
    outputs.push(max_joltage);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
