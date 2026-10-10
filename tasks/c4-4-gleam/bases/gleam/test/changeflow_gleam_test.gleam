import gleeunit
import gleeunit/should

pub fn main() {
  gleeunit.main()
}

pub fn base_keeps_an_identifier_example_test() {
  should.equal(2, 1 + 1)
}
