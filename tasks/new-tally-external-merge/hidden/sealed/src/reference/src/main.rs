use std::path::Path;
fn run()->Result<(),Box<dyn std::error::Error>>{
 let mut args=std::env::args().skip(1);let mut format="text".to_owned();let mut top=10usize;let mut memory=10000usize;let mut checkpoint=None;let mut files=vec![];
 while let Some(a)=args.next(){match a.as_str(){
  "--format"=>format=args.next().ok_or("missing format")?,
  "--top"=>top=args.next().ok_or("missing top")?.parse()?,
  "--memory-keys"=>memory=args.next().ok_or("missing memory limit")?.parse()?,
  "--checkpoint"=>checkpoint=Some(args.next().ok_or("missing checkpoint directory")?),
  "-"=>files.push(a),
  x if x.starts_with('-')=>return Err("unknown option".into()),
  _=>files.push(a)
 }}
 if !["text","json"].contains(&format.as_str()){return Err("invalid format".into())}
 let best=tally::external::count(&files,top,memory,checkpoint.as_deref().map(Path::new))?;
 if format=="json"{println!("{}",tally::output::render_json(&best))}else{print!("{}",tally::output::render_text(&best))}Ok(())
}
fn main(){if let Err(e)=run(){eprintln!("tally: {e}");std::process::exit(1)}}
