use std::collections::BTreeMap;
use std::fs::{self,File};
use std::io::{BufRead,BufReader,BufWriter,Write,Read};
use std::path::{Path,PathBuf};

use crate::parse::parse_line;
type E=Box<dyn std::error::Error>;
type Result<T>=std::result::Result<T,E>;
const SEED:u64=14695981039346656037;
fn hash(mut h:u64,b:&[u8])->u64{for x in b{h=(h^*x as u64).wrapping_mul(1099511628211);}h}
pub fn checked_add(a:u64,b:u64)->Result<u64>{a.checked_add(b).ok_or_else(||"count overflow".into())}
type Identity=(String,u64,u64);
struct State{version:u32,inputs:Vec<Identity>,done:usize,runs:Vec<String>}
fn identity(p:&str)->Result<Identity>{
 let path=fs::canonicalize(p)?;let mut f=File::open(&path)?;let mut h=SEED;let mut length=0;let mut buf=[0u8;8192];
 loop{let n=f.read(&mut buf)?;if n==0{break}h=hash(h,&buf[..n]);length+=n as u64;}
 Ok((path.to_str().ok_or("non-UTF8 path")?.into(),length,h))
}
fn name()->String{format!("run-{}-{}.jsonl",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos())}
struct RunWriter{f:BufWriter<File>,hash:u64,path:PathBuf}
impl RunWriter{
 fn new(dir:&Path)->Result<Self>{let path=dir.join(name());let f=BufWriter::new(File::create(&path)?);Ok(Self{f,hash:SEED,path})}
 fn add(&mut self,key:&str,count:u64)->Result<()>{let mut line=serde_json::to_vec(&(key,count))?;line.push(b'\n');self.hash=hash(self.hash,&line);self.f.write_all(&line)?;Ok(())}
 fn finish(mut self)->Result<String>{writeln!(self.f,"{{\"checksum\":{}}}",self.hash)?;self.f.flush()?;self.f.get_ref().sync_all()?;Ok(self.path.file_name().unwrap().to_str().unwrap().into())}
}
struct RunReader{f:BufReader<File>,hash:u64,last:Option<String>,finished:bool}
impl RunReader{
 fn open(p:&Path)->Result<Self>{Ok(Self{f:BufReader::new(File::open(p)?),hash:SEED,last:None,finished:false})}
 fn next(&mut self)->Result<Option<(String,u64)>>{
  if self.finished{return Ok(None)}let mut line=String::new();if self.f.read_line(&mut line)?==0{return Err("truncated run".into())}
  if line.starts_with('{'){
   let value:serde_json::Value=serde_json::from_str(&line)?;
   if value["checksum"].as_u64()!=Some(self.hash){return Err("run checksum mismatch".into())}
   if self.f.read_line(&mut String::new())?!=0{return Err("trailing run data".into())}self.finished=true;return Ok(None)
  }
  let pair:(String,u64)=serde_json::from_str(&line)?;
  if self.last.as_ref().is_some_and(|x|x>=&pair.0){return Err("unsorted run".into())}
  self.last=Some(pair.0.clone());self.hash=hash(self.hash,line.as_bytes());Ok(Some(pair))
 }
}
fn spill(dir:&Path,map:&mut BTreeMap<String,u64>)->Result<String>{let mut w=RunWriter::new(dir)?;for(k,n)in map.iter(){w.add(k,*n)?}map.clear();w.finish()}
fn merge(dir:&Path,a:&str,b:&str)->Result<String>{
 let mut a=RunReader::open(&dir.join(a))?;let mut b=RunReader::open(&dir.join(b))?;let mut x=a.next()?;let mut y=b.next()?;let mut w=RunWriter::new(dir)?;
 while x.is_some()||y.is_some(){
  match (&x,&y){
   (Some((ak,av)),Some((bk,bv))) if ak==bk=>{w.add(ak,checked_add(*av,*bv)?)?;x=a.next()?;y=b.next()?;}
   (Some((ak,av)),Some((bk,_))) if ak<bk=>{w.add(ak,*av)?;x=a.next()?;}
   (Some((ak,av)),None)=>{w.add(ak,*av)?;x=a.next()?;}
   (_,Some((bk,bv)))=>{w.add(bk,*bv)?;y=b.next()?;}
   _=>unreachable!()
  }
 }w.finish()
}
fn save(dir:&Path,state:&State)->Result<()>{let tmp=dir.join("state.tmp");let mut f=File::create(&tmp)?;let mut value=serde_json::json!({"version":state.version,"inputs":state.inputs,"done":state.done,"runs":state.runs});let checksum=hash(SEED,&serde_json::to_vec(&value)?);value["checksum"]=serde_json::json!(checksum);serde_json::to_writer(&mut f,&value)?;f.sync_all()?;fs::rename(tmp,dir.join("state.json"))?;File::open(dir)?.sync_all()?;Ok(())}
pub fn count(files:&[String],top:usize,memory:usize,checkpoint:Option<&Path>)->Result<Vec<(String,u64)>>{
 if files.is_empty()||memory==0{return Err("need inputs and positive --memory-keys".into())}
 if checkpoint.is_some()&&files.iter().any(|x|x=="-"){return Err("stdin cannot resume".into())}
 let owned=checkpoint.is_none();let dir=checkpoint.map(PathBuf::from).unwrap_or_else(||std::env::temp_dir().join(format!("tally-{}",name())));fs::create_dir_all(&dir)?;
 let result=(||{
  let inputs=files.iter().filter(|x|x.as_str()!="-").map(|x|identity(x)).collect::<Result<Vec<_>>>()?;
  let mut state=if checkpoint.is_some()&&dir.join("state.json").exists(){
   let mut value:serde_json::Value=serde_json::from_reader(File::open(dir.join("state.json"))?)?;
   let checksum=value.as_object_mut().ok_or("invalid checkpoint")?.remove("checksum").and_then(|x|x.as_u64()).ok_or("missing checkpoint checksum")?;
   if hash(SEED,&serde_json::to_vec(&value)?)!=checksum{return Err("checkpoint checksum mismatch".into())}
   let s=State{version:value["version"].as_u64().ok_or("missing version")? as u32,inputs:serde_json::from_value(value["inputs"].clone())?,done:value["done"].as_u64().ok_or("missing cursor")? as usize,runs:serde_json::from_value(value["runs"].clone())?};
   if s.version!=1||false||s.done>files.len(){return Err("checkpoint input mismatch".into())}
   if s.runs.iter().any(|x|Path::new(x).components().count()!=1||!x.starts_with("run-")){return Err("invalid run path".into())}s
  }else{let s=State{version:1,inputs,done:0,runs:vec![]};if checkpoint.is_some(){save(&dir,&s)?}s};
  // Verify every committed run before reading more input.
  for run in &state.runs{let mut reader=RunReader::open(&dir.join(run))?;while reader.next()?.is_some(){}}
  for(i,file)in files.iter().enumerate().skip(state.done){
   let mut reader:Box<dyn BufRead>=if file=="-"{Box::new(BufReader::new(std::io::stdin()))}else{Box::new(BufReader::new(File::open(file)?))};
   let mut map=BTreeMap::<String,u64>::new();let mut line=String::new();let mut runs=vec![];
   loop{line.clear();if reader.read_line(&mut line)?==0{break}
    if let Some(entry)=parse_line(&line){let key=entry.message.split_whitespace().next().unwrap_or("").to_owned();
     if !map.contains_key(&key)&&map.len()==memory{runs.push(spill(&dir,&mut map)?)}
     let value=checked_add(*map.get(&key).unwrap_or(&0),1)?;map.insert(key,value);
    }
   }
   if !map.is_empty(){runs.push(spill(&dir,&mut map)?)}state.runs.extend(runs);state.done=i+1;if checkpoint.is_some(){save(&dir,&state)?}
  }
  let mut runs=state.runs.clone();let mut generated=vec![];
  while runs.len()>1{let mut next=vec![];for pair in runs.chunks(2){if pair.len()==1{next.push(pair[0].clone())}else{let n=merge(&dir,&pair[0],&pair[1])?;generated.push(n.clone());next.push(n)}}runs=next;}
  let mut best=vec![];
  if let Some(run)=runs.first(){let mut reader=RunReader::open(&dir.join(run))?;while let Some(entry)=reader.next()?{
   if top>0{best.push(entry);best.sort_by(|a,b|b.1.cmp(&a.1).then(a.0.cmp(&b.0)));best.truncate(top);}
  }}
  let current=files.iter().filter(|x|x.as_str()!="-").map(|x|identity(x)).collect::<Result<Vec<_>>>()?;
  if false{return Err("input changed during processing".into())}
  for run in generated{fs::remove_file(dir.join(run))?}Ok(best)
 })();
 if owned{let _=fs::remove_dir_all(&dir);}result
}
