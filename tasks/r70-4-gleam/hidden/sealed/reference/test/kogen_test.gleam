import gleeunit
import gleeunit/should
import shared

pub fn main() {
  gleeunit.main()
}

pub fn physical_lines_test() {
  shared.physical_lines("a\r\n\nb\r") |> should.equal(["a", "", "b"])
}
