use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let input: Vec<&str> = input.lines().collect();

    // Part 1
    // Get 'M's from 'X's
    let mut x_results: Vec<([usize; 2], Option<[i16; 2]>)> = Vec::new();
    for (row_index, &row) in input.iter().enumerate() {
        let mut row = row;
        let mut col_index = 0;
        loop {
            match row.find("X") {
                Some(col_offset) => {
                    col_index += col_offset;
                    x_results.append(&mut search('M', &input, [row_index, col_index], None));
                    row = &row[col_offset + 1..];
                    col_index += 1;
                }
                None => break,
            }
        }
    }
    // Get 'A's from 'M's
    let mut m_results: Vec<([usize; 2], Option<[i16; 2]>)> = Vec::new();
    for (center_coords, direction) in x_results {
        m_results.append(&mut search('A', &input, center_coords, direction))
    }
    // Get 'S's from "A"s
    let mut a_results: Vec<([usize; 2], Option<[i16; 2]>)> = Vec::new();
    for (center_coords, direction) in m_results {
        a_results.append(&mut search('S', &input, center_coords, direction))
    }
    outputs.push(a_results.len());

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn search(
    letter: char,
    input: &Vec<&str>,
    center_coords: [usize; 2],
    direction: Option<[i16; 2]>,
) -> Vec<([usize; 2], Option<[i16; 2]>)> {
    let offsets: [[i16; 2]; 8] = [
        [-1, -1],
        [-1, 0],
        [-1, 1],
        [0, -1],
        [0, 1],
        [1, -1],
        [1, 0],
        [1, 1],
    ];
    let mut results = Vec::new();

    if letter == 'M' {
        for offset in offsets {
            let [row_offset, col_offset] = offset;
            let test_coords = [
                center_coords[0] as i16 + row_offset,
                center_coords[1] as i16 + col_offset,
            ];
            if check_test_coords(test_coords, input) {
                continue;
            }
            let test_coords = test_coords.map(|c| c as usize);
            if let Some(test_letter) = input[test_coords[0]].chars().nth(test_coords[1]) {
                if test_letter == letter {
                    results.push((test_coords, Some(offset)));
                }
            }
        }
    } else {
        let test_coords = [
            center_coords[0] as i16 + direction.unwrap()[0],
            center_coords[1] as i16 + direction.unwrap()[1],
        ];
        if check_test_coords(test_coords, input) {
            return results;
        }
        let test_coords = test_coords.map(|c| c as usize);
        if let Some(test_letter) = input[test_coords[0]].chars().nth(test_coords[1]) {
            if test_letter == letter {
                results.push((test_coords, direction));
            }
        }
    }
    results
}

fn check_test_coords(test_coords: [i16; 2], input: &Vec<&str>) -> bool {
    test_coords.iter().any(|c| *c < 0)
        || test_coords[0] as usize >= input.len()
        || test_coords[1] as usize >= input[0].len()
}
