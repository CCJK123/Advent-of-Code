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
        .collect::<Vec<[[i64; 2]; 3]>>();

    // Part 1
    outputs.push(calculate_tokens(&input));

    // Part 2
    let machines = input
        .iter()
        .map(|[a, b, [p_x, p_y]]| [*a, *b, [p_x + 10000000000000, p_y + 10000000000000]])
        .collect::<Vec<_>>();
    outputs.push(calculate_tokens(&machines));

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

/// **Formula Derivation**
///
/// Let the input coordinates for button A, button B and prize be (a_x, a_y),
/// (b_x, b_y) and (p_x, p_y) respectively.
/// Let A and B be the number of times buttons A and B are pressed respectively.
///
/// To solve: `A*a_x + B*b_x = p_x (1)` and `A*a_y + B*b_y = p_y (2)`
///
/// `(1) * b_y`: `A*a_x*b_y + B*b_x*b_y = p_x*b_y` => `B*b_x*b_y = p_x*b_y - A*a_x*b_y (3)`
///
/// `(2) * b_x`: `A*a_y*b_x + B*b_x*b_y = p_y*b_x` => `B*b_x*b_y = p_y*b_x - A*a_y*b_x (4)`
///
/// `(3) = (4)`: `p_x*b_y - A*a_x*b_y = p_y*b_x - A*a_y*b_x`
///           => `A * (a_x*b_y - a_y*b_x) = p_x*b_y - p_y*b_x`
///
/// ∴ `A = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)`
///
/// Similarly for B, `∴ B = (p_x*a_y - p_y*a_x) / (b_x*a_y - b_y*a_x) = (p_y*a_x - p_x*a_y) / (a_x*b_y - a_y*b_x)`
///
/// (Alternatively, use [Cramer's rule](https://en.wikipedia.org/wiki/Cramer's_rule)
/// directly instead of deriving the formula yourself, to obtain solutions for A and B)
fn calculate_tokens(input: &Vec<[[i64; 2]; 3]>) -> i64 {
    let mut tokens = 0;
    for [button_a, button_b, prize] in input {
        let a_numerator = prize[0] * button_b[1] - prize[1] * button_b[0];
        let b_numerator = prize[1] * button_a[0] - prize[0] * button_a[1];
        let denominator = button_a[0] * button_b[1] - button_a[1] * button_b[0];
        assert_ne!(denominator, 0); // Assume pair of linear equations has one unique solution
        if a_numerator % denominator == 0 && b_numerator % denominator == 0 {
            // Integer solutions exist for pair of linear equations, hence prize is winnable
            let a_count = a_numerator / denominator;
            let b_count = b_numerator / denominator;
            tokens += 3 * a_count + b_count;
        }
    }
    tokens
}
