use std::io::{self, Write};

pub fn prompt(msg: &str) -> Result<String, io::Error> {
    let mut input = String::new();
    print!("{}", msg);
    io::stdout().flush()?;
    io::stdin().read_line(&mut input)?;
    input.truncate(input.trim_end_matches(['\r', '\n']).len());
    Ok(input)
}

pub fn yn_prompt(msg: &str) -> bool {
    let response = prompt(msg).expect("Failed to get input");
    response == "" || ["Y", "y"].contains(&response.as_str())
}
