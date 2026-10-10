import gleam/int
import gleeunit
import gleeunit/should

pub fn main() {
  gleeunit.main()
}

pub fn termination_status_test() {
  128 + 15 |> should.equal(143)
}

pub fn integer_argument_test() {
  int.parse("600") |> should.equal(Ok(600))
}
