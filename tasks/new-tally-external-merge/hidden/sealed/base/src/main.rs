use std::io::Read;
use tally::agg::Aggregator;
use tally::output::{render_json, render_text};
use tally::parse::parse_line;

fn main() {
    let mut args = std::env::args().skip(1);
    let mut format = "text".to_string();
    let mut file = None;
    while let Some(a) = args.next() {
        match a.as_str() {
            "--format" => format = args.next().unwrap(),
            _ => file = Some(a),
        }
    }
    let file = file.expect("no file given");
    let text = if file == "-" {
        let mut s = String::new();
        std::io::stdin().read_to_string(&mut s).unwrap();
        s
    } else {
        std::fs::read_to_string(&file).unwrap()
    };
    let mut agg = Aggregator::default();
    for line in text.lines() {
        if let Some(e) = parse_line(line) {
            let key = e.message.split_whitespace().next().unwrap_or("");
            agg.add(key);
        }
    }
    let top = agg.top(10);
    match format.as_str() {
        "json" => println!("{}", render_json(&top)),
        _ => print!("{}", render_text(&top)),
    }
}
