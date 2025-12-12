use std::error::Error;

use itertools::Itertools;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    let red_tiles = input
        .lines()
        .map(|s| {
            let mut v = s.split(",").map(|x| x.parse::<u64>().unwrap());
            [v.next().unwrap(), v.next().unwrap()]
        })
        .collect_vec();

    // Part 1
    let possible_rectangle_areas =
        red_tiles
            .iter()
            .combinations(2)
            .map(|v| [v[0], v[1]])
            .map(|[tile_1, tile_2]| {
                (0..=1)
                    .map(|i| tile_1[i].abs_diff(tile_2[i]) + 1)
                    .product::<u64>()
            });
    let largest_area = possible_rectangle_areas.max().unwrap();
    outputs.push(largest_area);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
