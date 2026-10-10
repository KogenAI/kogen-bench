-module(queue_ffi).
-export([write_stderr/1]).

write_stderr(Text) ->
    _ = io:put_chars(standard_error, Text),
    nil.
