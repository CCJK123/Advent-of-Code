use std::{
    collections::{BTreeSet, HashMap},
    error::Error,
};

pub fn run(input: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Initial setup
    let mut outputs = Vec::new();
    #[derive(PartialEq, Eq, PartialOrd, Ord, Hash, Clone)]
    struct Button(Vec<u16>);
    struct Machine {
        target_lights: Vec<bool>,
        buttons: Vec<Button>,
        _joltage_reqs: Vec<u16>,
    }
    let machines = input
        .lines()
        .map(|s| {
            let s = s.replace("] (", "]|(").replace(") {", ")|{");
            let i = s.split('|').collect::<Vec<_>>();
            Machine {
                target_lights: i[0][1..(i[0].len() - 1)]
                    .chars()
                    .map(|c| c == '#')
                    .collect(),
                buttons: i[1]
                    .split(' ')
                    .map(|s| {
                        Button(
                            s[1..(s.len() - 1)]
                                .split(',')
                                .map(|s| s.parse().unwrap())
                                .collect(),
                        )
                    })
                    .collect(),
                _joltage_reqs: i[2][1..(i[2].len() - 1)]
                    .split(',')
                    .map(|s| s.parse().unwrap())
                    .collect(),
            }
        })
        .collect::<Vec<_>>();

    // Part 1
    let mut total = 0;
    for machine in machines.iter() {
        let mut previous_states = HashMap::<BTreeSet<Button>, Vec<bool>>::new();
        previous_states.insert(
            BTreeSet::new(),
            machine.target_lights.iter().map(|_| false).collect(),
        );
        let mut current_depth = 0;
        'main: loop {
            current_depth += 1;
            let mut new_states = HashMap::new();
            for (buttons_pressed, lights) in previous_states.iter() {
                for button_to_press in machine
                    .buttons
                    .iter()
                    // Press each button max once, since >=2 presses is counterproductive
                    .filter(|b| !buttons_pressed.contains(b))
                {
                    let mut new_buttons_pressed = buttons_pressed.clone();
                    new_buttons_pressed.insert(button_to_press.clone());
                    new_states.entry(new_buttons_pressed).or_insert({
                        let new_lights = lights
                            .iter()
                            .enumerate()
                            .map(|(i, &v)| button_to_press.0.contains(&(i as u16)) ^ v)
                            .collect::<Vec<_>>();
                        if new_lights == machine.target_lights {
                            break 'main;
                        }
                        new_lights
                    });
                }
            }
            previous_states = new_states;
        }
        total += current_depth;
    }
    outputs.push(total);

    Ok(outputs.iter().map(|s| s.to_string()).collect())
}
