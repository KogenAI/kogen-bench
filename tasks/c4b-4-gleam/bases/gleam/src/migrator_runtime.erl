-module(migrator_runtime).
-export([args/0, emit/1, abort/2]).

args() -> [unicode:characters_to_binary(A) || A <- init:get_plain_arguments()].
emit(Text) ->
    io:setopts(standard_io, [{encoding, unicode}]),
    io:put_chars(standard_io, [Text, <<"\n">>]), nil.
abort(Code, Text) ->
    io:setopts(standard_error, [{encoding, unicode}]),
    io:put_chars(standard_error, [Text, <<"\n">>]), erlang:halt(Code).
