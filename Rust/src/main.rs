use dashmap::DashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;
use std::error::Error;
use std::fs;
use std::io::Write;
use walkdir::{DirEntry, WalkDir};
use rayon::prelude::*;
use sha2::{Sha256, Digest};
use csv::Writer;

static COUNTER: AtomicUsize = AtomicUsize::new(0);

fn main() -> Result<(), Box<dyn Error>> {
    let start_time = Instant::now();
    let root_dir = "C:\\Users\\tmric\\Documents\\OneDrive";
    println!("Starting to walk directory: {}", root_dir);

    let file_hashes = DashMap::new();
    let visited_dirs = DashMap::new();
    walk_directory(root_dir, &file_hashes, &visited_dirs)?;

    let mut writer = Writer::from_path("file_hashes.csv")?;
    for entry in file_hashes.iter() {
        writer.write_record(&[entry.key(), entry.value()])?;
    }

    println!("Total files processed: {}", COUNTER.load(Ordering::SeqCst));
    println!("Time taken: {:?}", Instant::now() - start_time);

    Ok(())
}

fn hash_file(file_path: &str, file_hashes: &DashMap<String, String>) -> Result<String, Box<dyn Error>> {
    if let Some(hash) = file_hashes.get(file_path) {
        return Ok(hash.clone());
    }

    let bytes = fs::read(file_path)?;
    let mut hasher = Sha256::new();
    hasher.update(&bytes);
    let hash = hex::encode(hasher.finalize());
    file_hashes.insert(file_path.to_string(), hash.clone());
    COUNTER.fetch_add(1, Ordering::SeqCst);

    Ok(hash)
}

fn walk_directory(dir_path: &str, file_hashes: &DashMap<String, String>, visited_dirs: &DashMap<String, ()>) -> Result<(), Box<dyn Error>> {
    //println!("Walking directory: {}", dir_path);

    if !visited_dirs.contains_key(dir_path) {
        visited_dirs.insert(dir_path.to_string(), ());
        let entries: Vec<_> = WalkDir::new(dir_path)
            .into_iter()
            .filter_map(|e| e.ok())
            .collect();

        entries.par_iter().for_each(|entry| {
            let path = entry.path().to_str().unwrap().to_string();
            if entry.file_type().is_dir() {
                walk_directory(&path, file_hashes, visited_dirs).unwrap();
            } else {
                hash_file(&path, file_hashes).unwrap();
            }
        });
    }

    Ok(())
}
