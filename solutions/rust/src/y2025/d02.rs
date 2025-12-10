use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let ranges = input
        .split(",")
        .map(|range| {
            let mut range = range.split("-");
            [
                range.next().unwrap().parse().unwrap(),
                range.next().unwrap().parse().unwrap(),
            ]
        })
        .collect::<Vec<[u64; 2]>>();

    // Part 1
    let mut sum = 0;
    for [lower_bound, upper_bound] in ranges.iter() {
        let possible_lengths = (lower_bound.to_string().len()..=upper_bound.to_string().len())
            .filter(|length| length % 2 == 0);

        for length in possible_lengths {
            let length = length as u32;

            // Get bounds for a specific length
            let lower_bound = (*lower_bound).max(10_u64.pow(length - 1));
            let upper_bound = (*upper_bound).min(10_u64.pow(length) - 1);
            assert_eq!(lower_bound.to_string().len() as u32, length);
            assert_eq!(upper_bound.to_string().len() as u32, length);

            // Get left and right halves of respective bounds for subsequent calculations
            let lower_bound_left = lower_bound / 10_u64.pow(length / 2);
            let lower_bound_right = lower_bound % 10_u64.pow(length / 2);
            let upper_bound_left = upper_bound / 10_u64.pow(length / 2);
            let upper_bound_right = upper_bound % 10_u64.pow(length / 2);

            // Calculate sum of invalid IDs accordingly
            sum +=
                (lower_bound_left..=upper_bound_left).sum::<u64>() * (10_u64.pow(length / 2) + 1);
            if lower_bound_left < lower_bound_right {
                sum -= lower_bound_left * (10_u64.pow(length / 2) + 1)
            }
            if upper_bound_left > upper_bound_right {
                sum -= upper_bound_left * (10_u64.pow(length / 2) + 1)
            }
        }
    }
    outputs.push(sum);

    // Part 2
    let mut sum = 0;
    for [lower_bound, upper_bound] in ranges.iter() {
        let possible_lengths = lower_bound.to_string().len()..=upper_bound.to_string().len();

        for length in possible_lengths {
            let length = length as u32;

            // Get bounds for a specific length
            let lower_bound = (*lower_bound).max(10_u64.pow(length - 1));
            let upper_bound = (*upper_bound).min(10_u64.pow(length) - 1);
            assert_eq!(lower_bound.to_string().len() as u32, length);
            assert_eq!(upper_bound.to_string().len() as u32, length);

            // Instantiate variable to store invalid IDs to prevent double-counting
            let mut invalid_ids = vec![];

            // Get valid repeating sub-IDs and sum accordingly
            let possible_sub_lengths = (1..=length / 2).filter(|x| length % x == 0);
            for sub_length in possible_sub_lengths {
                let lower_bound_chunk: u64 = lower_bound.to_string()[..sub_length as usize]
                    .parse()
                    .unwrap();
                let upper_bound_chunk: u64 = upper_bound.to_string()[..sub_length as usize]
                    .parse()
                    .unwrap();

                let multiplier = ("0".repeat(sub_length as usize - 1) + "1")
                    .repeat((length / sub_length) as usize)
                    .parse::<u64>()
                    .unwrap();
                invalid_ids.extend(
                    (lower_bound_chunk..=upper_bound_chunk)
                        .map(|x| x * multiplier)
                        .filter(|x| {
                            !invalid_ids.contains(x) && x >= &lower_bound && x <= &upper_bound
                        })
                        .collect::<Vec<_>>(),
                );
            }

            sum += invalid_ids.iter().sum::<u64>();
        }
    }
    outputs.push(sum);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
