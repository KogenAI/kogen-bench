//! C ABI over the aggregator, shaped like a NIF boundary (opaque handle, C strings).
//! Real Rustler bindings would wrap the same calls; kept as plain `extern "C"` so `cargo test` needs no BEAM.
use crate::agg::Aggregator;
use std::ffi::{CStr, CString, c_char, c_int};

pub struct TallyHandle {
    agg: Aggregator,
}

#[unsafe(no_mangle)]
pub extern "C" fn tally_new() -> *mut TallyHandle {
    Box::into_raw(Box::new(TallyHandle { agg: Aggregator::default() }))
}

/// # Safety
/// `h` must come from `tally_new`; `key` must be a NUL-terminated string.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn tally_add(h: *mut TallyHandle, key: *const c_char) -> c_int {
    let h = unsafe { &mut *h };
    let key = unsafe { CStr::from_ptr(key) }.to_str().unwrap();
    h.agg.add(key);
    0
}

/// Returns the top `k` keys as `key=count\n` lines.
///
/// # Safety
/// `h` must come from `tally_new`.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn tally_top(h: *const TallyHandle, k: usize) -> *const c_char {
    let h = unsafe { &*h };
    let mut s = String::new();
    for (key, count) in h.agg.top(k) {
        s.push_str(&format!("{key}={count}\n"));
    }
    CString::new(s).unwrap().as_ptr()
}

/// # Safety
/// `h` must come from `tally_new` and not be used afterwards.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn tally_free(h: *mut TallyHandle) {
    drop(unsafe { Box::from_raw(h) });
}
