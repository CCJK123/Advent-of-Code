use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let grid = input
        .lines()
        .map(|l| l.chars().collect::<Vec<char>>())
        .collect::<Vec<_>>();

    // Part 1
    let mut roll_count = 0;
    for i in 0..(grid.len() as i32) {
        for j in 0..(grid[i as usize].len() as i32) {
            if grid[i as usize][j as usize] == '@' && check_accessibility(&grid, i, j) {
                roll_count += 1;
            }
        }
    }
    outputs.push(roll_count);

    // Part 2
    let mut roll_count = 0;
    let mut current_grid = grid.clone();
    let mut new_grid = grid.clone();
    loop {
        for i in 0..(current_grid.len() as i32) {
            for j in 0..(current_grid[i as usize].len() as i32) {
                if current_grid[i as usize][j as usize] == '@'
                    && check_accessibility(&current_grid, i, j)
                {
                    roll_count += 1;
                    new_grid[i as usize][j as usize] = '.';
                }
            }
        }

        if new_grid == current_grid {
            break;
        }
        current_grid = new_grid.clone();
    }
    outputs.push(roll_count);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn check_accessibility(grid: &Vec<Vec<char>>, i: i32, j: i32) -> bool {
    let mut adjacent_count = 0;
    let offsets = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0],
        [1, 1],
        [-1, -1],
        [1, -1],
        [-1, 1],
    ];
    for [x_offset, y_offset] in offsets {
        let new_i = i + x_offset;
        let new_j = j + y_offset;
        if new_i >= 0
            && new_i < grid.len() as i32
            && new_j >= 0
            && new_j < grid[i as usize].len() as i32
            && grid[new_i as usize][new_j as usize] == '@'
        {
            adjacent_count += 1;
        }
    }
    adjacent_count < 4
}
