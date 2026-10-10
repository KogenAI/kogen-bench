import config_migrator
import gleeunit
import gleeunit/should

pub fn main() {
  gleeunit.main()
}

pub fn identity_test() {
  config_migrator.identity() |> should.equal("config-migrator")
}

pub fn nonempty_test() {
  should.be_true(config_migrator.identity() != "")
}
