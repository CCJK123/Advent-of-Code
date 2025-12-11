mod utils;
mod y2024;
mod y2025;

use std::fs::{self, File};
use std::io::{ErrorKind, Write};
use std::process::Command;

use crate::utils::{prompt, yn_prompt};

fn main() {
    // Get puzzle solution to run
    let year = "2025";
    let day = prompt("Run which day's code? (1-25): ")
        .expect("Failed to get user input")
        .parse::<u8>()
        .expect("Invalid number");
    if day == 0u8 || day > 25u8 {
        panic!("Invalid day")
    }
    let day = &format!("{day:02}");

    // Get puzzle input
    let input_file_path = &format!("../../inputs/{year}/{day}.txt");
    let input = match fs::read_to_string(input_file_path) {
        Ok(i) => i,
        Err(e) => {
            assert_eq!(e.kind(), ErrorKind::NotFound);
            if yn_prompt("Input file doesn't exist. Create empty file? [Y/n]: ") {
                fs::create_dir_all(format!("../../inputs/{year}"))
                    .expect("Failed to create year module directory");
                File::options()
                    .write(true)
                    .create_new(true)
                    .open(input_file_path)
                    .expect("Failed to create input file");
                println!("File `{}` created", &input_file_path[6..]);
            } else {
                println!("Aborted");
                return;
            }
            String::new()
        }
    };

    // Run puzzle solution
    let outputs = match [year, day] {
        ["2024", "01"] => y2024::d01::run(&input),
        ["2024", "02"] => y2024::d02::run(&input),
        ["2024", "03"] => y2024::d03::run(&input),
        ["2024", "04"] => y2024::d04::run(&input),
        ["2024", "05"] => y2024::d05::run(&input),
        ["2024", "06"] => y2024::d06::run(&input),
        ["2024", "07"] => y2024::d07::run(&input),
        ["2024", "08"] => y2024::d08::run(&input),
        ["2024", "09"] => y2024::d09::run(&input),
        ["2024", "10"] => y2024::d10::run(&input),
        ["2024", "11"] => y2024::d11::run(&input),
        ["2024", "12"] => y2024::d12::run(&input),
        ["2024", "13"] => y2024::d13::run(&input),
        ["2024", "14"] => y2024::d14::run(&input),
        ["2024", "15"] => y2024::d15::run(&input),
        ["2025", "01"] => y2025::d01::run(&input),
        ["2025", "02"] => y2025::d02::run(&input),
        ["2025", "03"] => y2025::d03::run(&input),
        _ => {
            if yn_prompt(
                "Module containing puzzle solution might not exist. Create from template? [Y/n]: ",
            ) {
                // Create year module directory if it doesn't exist
                fs::create_dir_all(format!("src/y{year}"))
                    .expect("Failed to create year module directory");

                // Update year module file if it's missing contents (module definition of input day)
                let year_module_file_path = &format!("src/y{year}/mod.rs");
                let code_to_add = &format!("pub mod d{day};\n");
                if !(fs::exists(year_module_file_path)
                    .expect("Failed to check if year module file exists")
                    && fs::read_to_string(year_module_file_path)
                        .expect("Failed to read year module file")
                        .contains(code_to_add))
                {
                    let mut year_module_file = File::options()
                        .append(true)
                        .create(true)
                        .open(year_module_file_path)
                        .expect("Failed to open year module file");
                    year_module_file
                        .write_all(code_to_add.as_bytes())
                        .expect("Failed to update module file");
                    Command::new("rustfmt")
                        .arg(year_module_file_path)
                        .output()
                        .expect("Failed to format year module file");
                }

                // Create day module file (from template) if it doesn't exist
                let day_module_file_path = &format!("src/y{year}/d{day}.rs");
                if !fs::exists(day_module_file_path)
                    .expect("Failed to check if day module file exists")
                {
                    fs::copy("template.rs", day_module_file_path)
                        .expect("Failed to create day module file from template");
                }

                // Update `main.rs` file accordingly
                let main_file_path = "src/main.rs";
                let main_file_old = fs::read_to_string(main_file_path).unwrap();
                let mut main_file_new = String::new();
                let code_to_add = [
                    &format!("mod y{year};\n"),
                    &format!("        [\"{year}\", \"{day}\"] => y{year}::d{day}::run(&input),\n"),
                ];
                // Add module definition of year module if it doesn't exist
                if !main_file_old.contains(code_to_add[0]) {
                    main_file_new += code_to_add[0]
                }
                // Add match arm to run puzzle solution for given year and day if it doesn't exist
                let mut is_within_match = false;
                for line in main_file_old.lines() {
                    if line == code_to_add[0].trim_end_matches("\n") {
                        continue;
                    };
                    if line == "    let outputs = match [year, day] {" {
                        is_within_match = true;
                    } else if is_within_match
                        && (line == "        _ => {" || code_to_add[1].as_str() < line)
                    {
                        main_file_new += code_to_add[1];
                        is_within_match = false;
                    }
                    main_file_new += &format!("{line}\n");
                }
                let mut main_file = File::options()
                    .write(true)
                    .truncate(true)
                    .open(main_file_path)
                    .expect("Failed to open `main.rs` to update it");
                main_file
                    .write_all(main_file_new.as_bytes())
                    .expect("Failed to update `main.rs`");
                Command::new("rustfmt")
                    .arg(main_file_path)
                    .output()
                    .expect("Failed to format `main.rs`");
                Command::new("rustfmt").arg(main_file_path);
                println!("File `solutions/rust/{day_module_file_path}` created and module hierarchy updated accordingly");
            } else {
                println!("Aborted");
            }
            return;
        }
    }.expect("Puzzle solution error");

    // Print puzzle solution output
    if outputs.len() == 0 {
        println!("The code does not return anything!");
        return;
    }
    for (i, output) in outputs.iter().enumerate() {
        println!("Part {}: {output}", i + 1);
    }
}
