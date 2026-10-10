-module(landing_io).
-export([fail/2]).

fail(Code, Message) ->
    io:put_chars(standard_error, [Message, <<"\n">>]),
    erlang:halt(Code).
