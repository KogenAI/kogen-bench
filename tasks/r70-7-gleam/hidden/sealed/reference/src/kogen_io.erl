-module(kogen_io).
-export([args/0, read/1, write/1, fail/2, matches/2, position/2]).

args() -> [unicode:characters_to_binary(Arg) || Arg <- init:get_plain_arguments()].
read(Path) ->
    Result = case Path of
        none -> stdin();
        {some, <<"-">>} -> stdin();
        {some, File} -> file:read_file(File)
    end,
    case Result of
        {ok, Bytes} -> ascii(Bytes, 1, 1, Bytes);
        _ -> {error, unreadable}
    end.
stdin() ->
    io:setopts(standard_io, [binary, {encoding, latin1}]),
    chunks([]).
chunks(Acc) ->
    case io:get_chars(standard_io, "", 65536) of
        eof -> {ok, iolist_to_binary(lists:reverse(Acc))};
        {error, Reason} -> {error, Reason};
        Bytes -> chunks([Bytes | Acc])
    end.
ascii(<<>>, _, _, Whole) -> {ok, Whole};
ascii(<<Byte, _/binary>>, Line, Col, _) when Byte > 127 -> {error, {not_ascii, Line, Col}};
ascii(<<10, Rest/binary>>, Line, _, Whole) -> ascii(Rest, Line + 1, 1, Whole);
ascii(<<_, Rest/binary>>, Line, Col, Whole) -> ascii(Rest, Line, Col + 1, Whole).
write(Text) -> io:put_chars(standard_io, Text), nil.
fail(Code, Message) -> io:put_chars(standard_error, [Message, <<"\n">>]), erlang:halt(Code).
matches(Pattern, Text) -> re:run(Text, Pattern, [{capture, none}]) =:= match.
position(Text, Needle) ->
    case binary:match(Text, Needle) of {At, _} -> At; nomatch -> -1 end.
