use std::{collections::VecDeque, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    let block_count = input
        .chars()
        .step_by(2)
        .map(|c| c.to_digit(10).unwrap())
        .reduce(|acc, e| acc + e)
        .unwrap();
    let file_count: u32 = ((input.len() + 1) / 2).try_into().unwrap();

    let mut checksum: u64 = 0;
    let mut disk_map = input
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect::<VecDeque<_>>();
    let mut current_block_id = 0;
    let mut current_file_ids = [0, (file_count - 1) as u64];
    while current_block_id != block_count {
        // Deal with front blocks
        let front_file_block_count = disk_map.pop_front().unwrap();
        checksum +=
            block_id_range_sum(current_block_id, front_file_block_count) * current_file_ids[0];
        current_block_id += front_file_block_count;
        current_file_ids[0] += 1;

        // Adjust rear blocks
        let Some(mut empty_block_count) = disk_map.pop_front() else {
            break;
        };
        while current_block_id != block_count && empty_block_count != 0 {
            let rear_file_block_count = disk_map[disk_map.len() - 1];
            if empty_block_count >= rear_file_block_count {
                // Entire rear file can fit into empty block
                checksum += block_id_range_sum(current_block_id, rear_file_block_count)
                    * current_file_ids[1];
                current_block_id += rear_file_block_count;
                current_file_ids[1] -= 1;
                disk_map.pop_back();
                disk_map.pop_back();
                empty_block_count -= rear_file_block_count;
            } else {
                // Only part of rear file can fit into empty block
                checksum +=
                    block_id_range_sum(current_block_id, empty_block_count) * current_file_ids[1];
                current_block_id += empty_block_count;
                let disk_map_len = disk_map.len();
                disk_map[disk_map_len - 1] -= empty_block_count;
                empty_block_count = 0;
            }
        }
    }
    outputs.push(checksum);

    // Part 2
    let mut file_block_ranges = Vec::new();
    let mut empty_block_ranges = Vec::new();
    let mut current_block_id = 0;
    let mut is_file = true;
    for block_length in input.chars().map(|c| c.to_digit(10).unwrap()) {
        let range = [current_block_id, current_block_id + block_length];
        if is_file {
            file_block_ranges.push(range);
        } else if block_length != 0 {
            empty_block_ranges.push(range);
        }
        current_block_id = range[1];
        is_file = !is_file;
    }

    let mut checksum: u64 = 0;
    'a: for (file_id, file_block_range) in file_block_ranges.iter().enumerate().rev() {
        // Movable files
        for (i, empty_block_range) in empty_block_ranges.clone().iter().enumerate() {
            if empty_block_range[1] <= file_block_range[0]
                && block_range_size(empty_block_range) >= block_range_size(file_block_range)
            {
                // Modify fully/partially-filled empty block
                empty_block_ranges[i][0] =
                    empty_block_range[0] + block_range_size(file_block_range);
                if empty_block_ranges[i][0] == empty_block_ranges[i][1] {
                    empty_block_ranges.remove(i);
                }
                // Replace old file block range with empty block
                empty_block_ranges.push(*file_block_range);
                empty_block_ranges.sort();
                empty_block_ranges = empty_block_ranges.iter().fold(Vec::new(), |mut acc, e| {
                    if acc.len() != 0 && acc[acc.len() - 1][1] == e[0] {
                        let index = acc.len() - 1;
                        acc[index][1] = e[1];
                    } else {
                        acc.push(*e);
                    }
                    acc
                });
                // Update checksum accordingly
                checksum +=
                    block_id_range_sum(empty_block_range[0], block_range_size(file_block_range))
                        * file_id as u64;
                continue 'a;
            }
        }
        // Immovable files
        checksum += block_id_range_sum(
            file_block_range[0],
            file_block_range[1] - file_block_range[0],
        ) * file_id as u64;
    }
    outputs.push(checksum);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn block_id_range_sum(current_block_id: u32, block_count: u32) -> u64 {
    ((2 * current_block_id + block_count - 1) as f32 / 2f32 * block_count as f32) as u64
}

fn block_range_size(block_range: &[u32; 2]) -> u32 {
    block_range[1] - block_range[0]
}
