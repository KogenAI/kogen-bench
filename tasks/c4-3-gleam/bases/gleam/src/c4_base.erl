-module(c4_base).
-export([not_implemented/0]).
not_implemented() ->
    io:put_chars(standard_error, <<"{\"error\":{\"code\":\"NOT_IMPLEMENTED\",\"message\":\"implement run\"}}\n">>),
    erlang:halt(70).
