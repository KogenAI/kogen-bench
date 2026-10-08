-module(kogen_io).
-export([args/0, read/1, write/1, fail/2, matches/2, position/2, execute/1]).

execute(Args) ->
    try command(Args) of Text -> Text
    catch throw:{failure, Code, Message} -> fail(Code, Message) end.

command([<<"reconcile">>, <<"--log">>, Path]) -> reconcile(read_events(Path));
command([<<"append">>, <<"--log">>, Path, <<"--event">>, Raw]) -> append_event(Path, Raw);
command(_) -> throw({failure, 2, <<"eventlog: usage error">>}).

append_event(Path, Raw) ->
    Event = parse_event(Raw, 1),
    Old = case file:read_file(Path) of {ok, B} -> B; {error, enoent} -> <<>>; _ -> err(<<"eventlog: cannot access log">>) end,
    case byte_size(Old) > 0 andalso binary:last(Old) =/= 10 of true -> err(invalid(count_lf(Old) + 1)); false -> ok end,
    Events = read_events(Path),
    case [E || E <- Events, maps:get(id, E) =:= maps:get(id, Event)] of
        [Found | _] -> err(io_lib:format("eventlog:~B: duplicate event id '~s'", [maps:get(line, Found), maps:get(id, Event)]));
        [] -> ok
    end,
    Id = maps:get(id, Event), Type = maps:get(type, Event), Job = maps:get(job, Event), Ts = maps:get(ts, Event),
    IdJson = iolist_to_binary(json:encode(Id)),
    TypeJson = iolist_to_binary(json:encode(Type)),
    JobJson = iolist_to_binary(json:encode(Job)),
    Encoded = <<"{\"id\":", IdJson/binary, ",\"type\":", TypeJson/binary, ",\"job\":", JobJson/binary, ",\"ts\":", (integer_to_binary(Ts))/binary, "}\n">>,
    case file:write_file(Path, Encoded, [append]) of ok -> <<"appended ", Id/binary, "\n">>; _ -> err(<<"eventlog: cannot access log">>) end.

read_events(Path) ->
    Data = case file:read_file(Path) of {ok, B} -> B; {error, enoent} -> <<>>; _ -> err(<<"eventlog: cannot access log">>) end,
    Complete = complete_lines(Data),
    {Rev, _} = lists:foldl(fun({Line, N}, {Acc, Seen}) ->
        E = parse_event(Line, N), Id = maps:get(id, E),
        case maps:is_key(Id, Seen) of true -> err(io_lib:format("eventlog:~B: duplicate event id '~s'", [N, Id])); false -> {[E | Acc], maps:put(Id, true, Seen)} end
    end, {[], #{}}, lists:zip(Complete, lists:seq(1, length(Complete)))),
    lists:reverse(Rev).

complete_lines(<<>>) -> [];
complete_lines(Data) -> lists:droplast(binary:split(Data, <<"\n">>, [global])).

parse_event(Raw, Line) ->
    case duplicate_key(Raw) of true -> err(invalid(Line)); false -> ok end,
    Decoded = try json:decode(Raw) catch _:_ -> err(invalid(Line)) end,
    case is_map(Decoded) andalso map_size(Decoded) =:= 4 of true -> ok; false -> err(invalid(Line)) end,
    Id = maps:get(<<"id">>, Decoded, invalid), Type = maps:get(<<"type">>, Decoded, invalid), Job = maps:get(<<"job">>, Decoded, invalid), Ts = maps:get(<<"ts">>, Decoded, invalid),
    case is_binary(Id) andalso is_binary(Type) andalso is_binary(Job) andalso is_integer(Ts) andalso Ts >= 0 andalso Ts =< 9223372036854775807 of true -> ok; false -> err(invalid(Line)) end,
    case re:run(Id, <<"\\Ae-[a-z0-9]{1,16}\\z">>, [{capture, none}]) =:= match andalso re:run(Job, <<"\\A[a-z][a-z0-9-]{0,31}\\z">>, [{capture, none}]) =:= match of true -> ok; false -> err(invalid(Line)) end,
    case lists:member(Type, [<<"created">>, <<"started">>, <<"completed">>, <<"failed">>]) of true -> #{id => Id, type => Type, job => Job, ts => Ts, line => Line}; false -> err(io_lib:format("eventlog:~B: unknown event type '~s'", [Line, Type])) end.

duplicate_key(Raw) -> lists:any(fun(Key) ->
    Pattern = <<"\\\"", Key/binary, "\\\"\\s*:">>,
    case re:run(Raw, Pattern, [global, {capture, all, index}]) of {match, Matches} -> length(Matches) > 1; _ -> false end
end, [<<"id">>, <<"type">>, <<"job">>, <<"ts">>]).

reconcile(Events) ->
    Sorted = lists:sort(fun(A, B) -> {maps:get(ts,A), maps:get(line,A)} =< {maps:get(ts,B), maps:get(line,B)} end, Events),
    States = lists:foldl(fun(E, Acc) ->
        Job = maps:get(job,E), Type = maps:get(type,E), Ts = maps:get(ts,E), Line = maps:get(line,E), {Current, PreviousTs} = maps:get(Job, Acc, {<<>>, undefined}),
        case PreviousTs =:= Ts of true -> transition(Line, Job); false -> ok end,
        Next = case {Current, Type} of {<<>>, <<"created">>} -> <<"queued">>; {<<"queued">>, <<"started">>} -> <<"running">>; {<<"running">>, <<"completed">>} -> <<"done">>; {<<"running">>, <<"failed">>} -> <<"failed">>; _ -> transition(Line, Job) end,
        maps:put(Job, {Next, Ts}, Acc)
    end, #{}, Sorted),
    Values = [S || {_J, {S, _T}} <- maps:to_list(States)], Total = map_size(States),
    iolist_to_binary(io_lib:format("total=~B~nqueued=~B~nrunning=~B~ndone=~B~nfailed=~B~n", [Total, count(<<"queued">>,Values), count(<<"running">>,Values), count(<<"done">>,Values), count(<<"failed">>,Values)])).

count(Value, List) -> length([ok || X <- List, X =:= Value]).
transition(Line, Job) -> err(io_lib:format("eventlog:~B: invalid transition for job '~s'", [Line, Job])).
invalid(Line) -> io_lib:format("eventlog:~B: invalid event", [Line]).
count_lf(Bin) -> length(binary:matches(Bin, <<"\n">>)).
err(Message) -> throw({failure, 1, Message}).

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
