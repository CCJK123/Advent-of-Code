use std::{collections::VecDeque, error::Error};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    let mut checksum: u64 = 0;
    let block_count = input
        .chars()
        .step_by(2)
        .map(|c| c.to_digit(10).unwrap())
        .reduce(|acc, e| acc + e)
        .unwrap();
    let file_count: u32 = ((input.len() + 1) / 2).try_into().unwrap();

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
            get_block_id_range_sum(current_block_id, front_file_block_count) * current_file_ids[0];
        current_block_id += front_file_block_count;
        current_file_ids[0] += 1;

        // Adjust rear blocks
        let Some(mut empty_block_count) = disk_map.pop_front() else {
            break;
        };
        while empty_block_count != 0 {
            let rear_file_block_count = disk_map[disk_map.len() - 1];
            if empty_block_count >= rear_file_block_count {
                // Entire rear file can fit into empty block
                checksum += get_block_id_range_sum(current_block_id, rear_file_block_count)
                    * current_file_ids[1];
                current_block_id += rear_file_block_count;
                current_file_ids[1] -= 1;
                disk_map.pop_back();
                disk_map.pop_back();
                empty_block_count -= rear_file_block_count;
            } else {
                // Only part of rear file can fit into empty block
                checksum += get_block_id_range_sum(current_block_id, empty_block_count)
                    * current_file_ids[1];
                current_block_id += empty_block_count;
                let disk_map_len = disk_map.len();
                disk_map[disk_map_len - 1] -= empty_block_count;
                empty_block_count = 0;
            }
        }
    }

    // println!("{block_count}");
    // let mut blocks = Vec::new();

    outputs.push(checksum);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}

fn get_block_id_range_sum(current_block_id: u32, block_count: u32) -> u64 {
    ((2 * current_block_id + block_count - 1) as f32 / 2f32 * block_count as f32) as u64
}
