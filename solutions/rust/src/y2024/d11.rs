use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .split(" ")
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>();

    // Part 1
    let mut stones = input;
    for _ in 0..25 {
        stones = stones
            .iter()
            .map(|stone| {
                let mut result = Vec::new();
                if *stone == 0 {
                    result.push(1);
                } else if stone.checked_ilog10().unwrap_or(0) % 2 == 1 {
                    let stone_string = stone.to_string();
                    let (left, right) = stone_string.split_at(
                        ((stone.checked_ilog10().unwrap() + 1) / 2)
                            .try_into()
                            .unwrap(),
                    );
                    result.push(left.parse::<u64>().unwrap());
                    result.push(right.parse::<u64>().unwrap());
                } else {
                    result.push(stone * 2024)
                }
                result
            })
            .reduce(|mut acc, e| {
                acc.extend(e);
                acc
            })
            .unwrap();
    }
    outputs.push(stones.len());

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
