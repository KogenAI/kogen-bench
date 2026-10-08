//! Async ingest service: keys are submitted from many tasks and counted by one worker.
use crate::agg::Aggregator;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use tokio::sync::mpsc;
use tokio::task::JoinHandle;

#[derive(Debug, PartialEq, Eq)]
pub struct Closed;

#[derive(Clone)]
pub struct Submitter {
    tx: mpsc::Sender<String>,
}

impl Submitter {
    pub async fn submit(&self, key: impl Into<String>) -> Result<(), Closed> {
        self.tx.send(key.into()).await.map_err(|_| Closed)
    }
}

pub struct Service {
    tx: mpsc::Sender<String>,
    stop: Arc<AtomicBool>,
    worker: JoinHandle<Aggregator>,
}

async fn run(mut rx: mpsc::Receiver<String>, stop: Arc<AtomicBool>) -> Aggregator {
    let mut agg = Aggregator::default();
    while !stop.load(Ordering::Acquire) {
        match rx.recv().await {
            Some(key) => {
                agg.add(&key);
                tokio::task::yield_now().await;
            }
            None => break,
        }
    }
    agg
}

impl Service {
    /// Must be called inside a tokio runtime.
    pub fn start() -> Service {
        let (tx, rx) = mpsc::channel(64);
        let stop = Arc::new(AtomicBool::new(false));
        let worker = tokio::spawn(run(rx, stop.clone()));
        Service { tx, stop, worker }
    }

    pub fn submitter(&self) -> Submitter {
        Submitter { tx: self.tx.clone() }
    }

    pub async fn submit(&self, key: impl Into<String>) -> Result<(), Closed> {
        self.tx.send(key.into()).await.map_err(|_| Closed)
    }

    /// Stop the service and return what was counted.
    pub async fn shutdown(self) -> Aggregator {
        self.stop.store(true, Ordering::Release);
        drop(self.tx);
        self.worker.await.unwrap()
    }
}
