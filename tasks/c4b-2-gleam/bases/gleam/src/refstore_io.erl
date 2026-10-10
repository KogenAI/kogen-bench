-module(refstore_io).
-export([not_implemented/0]).
not_implemented() ->
    io:put_chars(standard_error, <<"{\"error\":{\"code\":\"NOT_IMPLEMENTED\",\"message\":\"Implement the store\"}}\n">>),
    erlang:halt(70).
