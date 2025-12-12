use std::{
    collections::{HashMap, HashSet},
    error::Error,
};

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

    // Part 2
    // Compress coordinates
    let mut coordinate_values = [HashSet::new(), HashSet::new()];
    for red_tile in red_tiles.iter() {
        for i in 0..=1 {
            coordinate_values[i].insert(red_tile[i]);
        }
    }
    let coordinate_values = [
        coordinate_values[0].iter().sorted().collect_vec(),
        coordinate_values[1].iter().sorted().collect_vec(),
    ];
    let red_tiles = red_tiles
        .iter()
        .map(|[x, y]| {
            [
                coordinate_values[0].iter().position(|i| *i == x).unwrap(),
                coordinate_values[1].iter().position(|i| *i == y).unwrap(),
            ]
        })
        .collect::<HashSet<_>>();

    // Sweep line to get interior (i.e. red/green) tiles
    let mut red_tile_x_lookup = HashMap::new();
    for [x, y] in red_tiles.iter() {
        red_tile_x_lookup
            .entry(x)
            .and_modify(|v: &mut Vec<_>| v.push(y))
            .or_insert(vec![y]);
    }
    red_tile_x_lookup.values_mut().for_each(|v| v.sort());

    assert_eq!(red_tile_x_lookup[&0].len(), 2);
    let mut interior_tiles = (*red_tile_x_lookup[&0][0]..=*red_tile_x_lookup[&0][1])
        .map(|y| [0, y])
        .collect::<HashSet<_>>();
    let mut exterior_tiles = HashSet::new();
    for (&&x, y_values) in red_tile_x_lookup.iter().sorted().skip(1) {
        assert_eq!(y_values.len() % 2, 0); // Even => Always have 90° turn at red tile / No connected collinear red tiles => Fewer cases
        assert_eq!(y_values.len() / 2, 1); // No need to handle multiples of 2

        // Find interior tiles
        for y in 0..coordinate_values[1].len() {
            if (y_values[0]..=y_values[1]).contains(&&y) // On line formed by connecting the two red tiles
                || (interior_tiles.contains(&[x - 1, y]) && !exterior_tiles.contains(&[x, y]))
            {
                interior_tiles.insert([x, y]);
            }
        }
        // Find some exterior tiles on next line for use next iteration
        if x != coordinate_values[0].len() - 1 {
            for y in 0..coordinate_values[1].len() {
                if interior_tiles.contains(&[x - 1, y]) // Tile above is an interior tile
                && ((y == *y_values[0] && (y == 0 || !interior_tiles.contains(&[x, y - 1]))) // Left convex corner
                    || (y == *y_values[1] && !interior_tiles.contains(&[x, y + 1])) // Right convex corner
                    || ((y_values[0] + 1)..*y_values[1]).contains(&&y) // Below middle portion of line
                ) {
                    exterior_tiles.insert([x + 1, y]);
                }
            }
        }
    }

    // Get new largest area
    let possible_rectangle_areas = red_tiles
        .iter()
        .combinations(2)
        .map(|v| [v[0], v[1]])
        .filter(|[tile_1, tile_2]| {
            // Filter out invalid rectangles
            (tile_1[0].min(tile_2[0])..=tile_1[0].max(tile_2[0]))
                .cartesian_product(tile_1[1].min(tile_2[1])..=tile_1[1].max(tile_2[1]))
                .all(|(x, y)| interior_tiles.contains(&[x, y]))
        })
        .map(|[tile_1, tile_2]| {
            (0..=1)
                .map(|i| {
                    coordinate_values[i][tile_1[i]].abs_diff(*coordinate_values[i][tile_2[i]]) + 1
                })
                .product::<u64>()
        });
    let largest_area = possible_rectangle_areas.max().unwrap();
    outputs.push(largest_area);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
