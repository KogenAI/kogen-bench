//! Word tokenizer: a word is a maximal run of alphanumeric characters, `_` or `'`.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Token {
    pub text: String,
    /// Byte offset of the word in the input.
    pub start: usize,
}

pub fn tokenize(input: &str) -> Vec<Token> {
    let is_word = |c: char| c.is_alphanumeric() || c == '_' || c == '\'';
    let mut out = Vec::new();
    let mut start: Option<usize> = None;
    for (i, c) in input.char_indices() {
        match (is_word(c), start) {
            (true, None) => start = Some(i),
            (false, Some(s)) => {
                out.push(Token { text: input[s..i].to_string(), start: s });
                start = None;
            }
            _ => {}
        }
    }
    if let Some(s) = start {
        out.push(Token { text: input[s..].to_string(), start: s });
    }
    out
}
