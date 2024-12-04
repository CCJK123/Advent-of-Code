use std::error::Error;

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();

    // Part 1
    let mut list_1 = Vec::<u32>::new();
    let mut list_2 = Vec::<u32>::new();
    for line in input.lines() {
        let mut entries = line.split("   ");
        list_1.push(entries.next().unwrap().parse()?);
        list_2.push(entries.next().unwrap().parse()?);
    }
    list_1.sort();
    list_2.sort();
    let mut total = 0;
    for i in 0..list_1.len() {
        total += list_1[i].abs_diff(list_2[i])
    }
    outputs.push(total);

    // Part 2
    let mut total = 0;
    for location_id in list_1 {
        total += location_id * list_2.iter().filter(|n| **n == location_id).count() as u32
    }
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
