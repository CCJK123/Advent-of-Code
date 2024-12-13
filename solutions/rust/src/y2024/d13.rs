use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input = input
        .lines()
        .fold(vec![Vec::new()], |mut acc, line| {
            if line.len() == 0 {
                acc.push(Vec::new());
            } else {
                let line = line.split(['+', '=']).collect::<Vec<&str>>();
                let acc_index = acc.len() - 1;
                acc[acc_index].push([
                    line[1][..line[1].len() - 3].parse().unwrap(),
                    line[2].parse().unwrap(),
                ]);
            }
            acc
        })
        .into_iter()
        .map(|v| [v[0], v[1], v[2]])
        .collect::<Vec<[[u32; 2]; 3]>>();

    // Part 1
    let mut tokens = 0;
    for [button_a, button_b, prize] in &input {
        let mut token_options = Vec::new();
        let max_a_count = (prize[0] / button_a[0])
            .min(prize[1] / button_a[1])
            .min(100);
        let max_b_count = (prize[0] / button_b[0])
            .min(prize[1] / button_b[1])
            .min(100);
        for a_count in 0..=max_a_count {
            for b_count in 0..=max_b_count {
                if *prize
                    == [
                        button_a[0] * a_count + button_b[0] * b_count,
                        button_a[1] * a_count + button_b[1] * b_count,
                    ]
                {
                    token_options.push(a_count * 3 + b_count);
                    break;
                }
            }
        }
        if let Some(min_tokens) = token_options.iter().min() {
            tokens += min_tokens;
        }
    }
    outputs.push(tokens);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
