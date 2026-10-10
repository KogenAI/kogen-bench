import gleeunit
import gleeunit/should
import shared

pub fn main() {
  gleeunit.main()
}

pub fn ordinary_name_test() {
  shared.valid_name("alpha_2-x") |> should.be_true
}

pub fn empty_name_test() {
  shared.valid_name("") |> should.be_false
}

pub fn traversal_name_test() {
  shared.valid_name("../bad") |> should.be_false
}
