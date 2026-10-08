//! Fixed-capacity byte ring buffer; pushing into a full buffer drops the oldest byte.

pub struct RingBuf {
    buf: Vec<u8>,
    head: usize,
    len: usize,
}

impl RingBuf {
    pub fn new(capacity: usize) -> RingBuf {
        RingBuf { buf: vec![0; capacity], head: 0, len: 0 }
    }

    pub fn capacity(&self) -> usize {
        self.buf.len()
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn push(&mut self, b: u8) {
        let cap = self.buf.len();
        let idx = (self.head + self.len) % cap;
        self.buf[idx] = b;
        if self.len == cap {
            self.head = (self.head + 1) % cap;
        } else {
            self.len += 1;
        }
    }

    pub fn pop(&mut self) -> Option<u8> {
        if self.len == 0 {
            return None;
        }
        let b = unsafe { *self.buf.get_unchecked(self.head) };
        self.head = (self.head + 1) % self.buf.len();
        self.len -= 1;
        Some(b)
    }

    /// The `i`-th oldest byte.
    pub fn peek(&self, i: usize) -> Option<u8> {
        if i >= self.buf.len() {
            return None;
        }
        Some(unsafe { *self.buf.get_unchecked(self.head + i) })
    }

    /// Contents, oldest first, as text.
    pub fn text(&self) -> String {
        let mut v = Vec::with_capacity(self.len);
        for i in 0..self.len {
            v.push(self.peek(i).unwrap());
        }
        unsafe { String::from_utf8_unchecked(v) }
    }
}
