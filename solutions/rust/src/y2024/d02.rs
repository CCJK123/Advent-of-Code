use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    let mut safe_count = 0;
    for report in input.lines() {
        let mut levels = report.split(" ").map(|n| n.parse::<u8>().unwrap());
        let mut level_old = levels.next().unwrap();
        let mut is_increasing = None;
        let mut is_safe = true;

        for level_new in levels {
            let safety_results = check_safety(level_old, level_new, is_increasing);
            is_increasing = safety_results.1;
            is_safe = is_safe && safety_results.0;
            level_old = level_new
        }
        if is_safe {
            safe_count += 1
        }
    }
    outputs.push(safe_count);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn check_safety(
    level_old: u8,
    level_new: u8,
    mut is_increasing: Option<bool>,
) -> (bool, Option<bool>) {
    // Check all increasing/decreasing
    match is_increasing {
        Some(is_increasing) => {
            if (is_increasing && level_old >= level_new)
                || (!is_increasing && level_old <= level_new)
            {
                return (false, Some(is_increasing));
            }
        }
        None => is_increasing = Some(level_new > level_old),
    }
    // Check 1 <= diff <= 3
    let diff = level_old.abs_diff(level_new);
    if diff < 1 || diff > 3 {
        return (false, is_increasing);
    }
    return (true, is_increasing);
}
