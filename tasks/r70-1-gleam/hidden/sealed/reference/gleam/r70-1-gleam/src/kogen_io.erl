-module(kogen_io).
-include_lib("kernel/include/file.hrl").
-export([args/0, read/1, write/1, fail/2, matches/2, position/2, queue/1]).

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

queue(Args) ->
    try
        Bins = [to_bin(A) || A <- Args],
        {Command, Values} = parse(Bins),
        Store = binary_to_list(maps:get(<<"--store">>, Values)),
        ok = filelib:ensure_dir(filename:join(Store, "x")),
        with_lock(Store, fun() -> dispatch(Command, Values, Store) end)
    catch
        throw:{kogen, Code, Message} -> fail(Code, Message);
        _:_ -> fail(4, "error: store failure")
    end.

to_bin(B) when is_binary(B) -> B;
to_bin(L) -> unicode:characters_to_binary(L).

parse([<<"queue">>, Command | Rest]) when Command =:= <<"add">>; Command =:= <<"run">>; Command =:= <<"status">> ->
    Allowed = case Command of <<"add">> -> [<<"--store">>, <<"--id">>, <<"--argv">>]; _ -> [<<"--store">>] end,
    Values = parse_options(Rest, Allowed, #{}),
    Store = maps:get(<<"--store">>, Values, <<>>),
    Valid = case Command of
        <<"add">> -> valid_id(maps:get(<<"--id">>, Values, <<>>)) andalso maps:get(<<"--argv">>, Values, <<>>) =/= <<>>;
        _ -> true
    end,
    case Store =/= <<>> andalso Valid of true -> {Command, Values}; false -> throw({kogen, 2, "error: invalid arguments"}) end;
parse(_) -> throw({kogen, 2, "error: invalid arguments"}).

parse_options([], _Allowed, Values) -> Values;
parse_options([Key, Value | Rest], Allowed, Values) ->
    case lists:member(Key, Allowed) andalso not maps:is_key(Key, Values) of
        true -> parse_options(Rest, Allowed, maps:put(Key, Value, Values));
        false -> throw({kogen, 2, "error: invalid arguments"})
    end;
parse_options(_, _, _) -> throw({kogen, 2, "error: invalid arguments"}).

valid_id(<<First, Rest/binary>>) when byte_size(Rest) < 64 ->
    alnum(First) andalso lists:all(fun(C) -> alnum(C) orelse C =:= $. orelse C =:= $_ orelse C =:= $- end, binary_to_list(Rest));
valid_id(_) -> false.
alnum(C) -> (C >= $A andalso C =< $Z) orelse (C >= $a andalso C =< $z) orelse (C >= $0 andalso C =< $9).

with_lock(Store, Fun) ->
    Lock = filename:join(Store, ".lockdir"),
    acquire(Lock, 0),
    try Fun() after file:delete(filename:join(Lock, "owner")), file:del_dir(Lock) end.
acquire(Lock, Wait) ->
    case file:make_dir(Lock) of
        ok ->
            Pid = os:getpid(),
            Owner = [Pid, "\n", boot_id(), "\n", process_start_time(Pid)],
            file:write_file(filename:join(Lock, "owner"), Owner, [sync]);
        {error, eexist} ->
            Owner = filename:join(Lock, "owner"),
            case file:read_file(Owner) of
                {ok, Pid} ->
                    case owner_alive(Pid) of
                        true -> timer:sleep(10), acquire(Lock, Wait + 1);
                        false -> file:delete(Owner), file:del_dir(Lock), acquire(Lock, Wait + 1)
                    end;
                _ when Wait > 100 -> file:del_dir(Lock), acquire(Lock, Wait + 1);
                _ -> timer:sleep(10), acquire(Lock, Wait + 1)
            end;
        _ -> throw({kogen, 4, "error: store failure"})
    end.
owner_alive(PidBin) ->
    case string:tokens(binary_to_list(PidBin), "\n") of
        [Pid, Boot, Start] -> Boot =:= boot_id() andalso process_start_time(Pid) =:= Start;
        _ -> false
    end.
boot_id() ->
    case file:read_file("/proc/sys/kernel/random/boot_id") of
        {ok, Id} -> string:trim(binary_to_list(Id));
        _ -> "unknown"
    end.
process_start_time(Pid) ->
    case file:read_file(filename:join(["/proc", Pid, "stat"])) of
        {ok, Stat} ->
            Matches = binary:matches(Stat, <<")">>),
            {At, 1} = lists:last(Matches),
            Tail = binary:part(Stat, At + 1, byte_size(Stat) - At - 1),
            case lists:nth(20, string:tokens(binary_to_list(Tail), " ")) of
                Start -> Start
            end;
        _ -> "dead"
    end.

dispatch(<<"add">>, Values, Store) ->
    Id = maps:get(<<"--id">>, Values),
    Jobs = load_jobs(Store),
    case lists:any(fun(J) -> maps:get(<<"id">>, J) =:= Id end, Jobs) of
        true -> throw({kogen, 3, "error: duplicate job id"});
        false -> ok
    end,
    Decoded = try json:decode(maps:get(<<"--argv">>, Values)) catch _:_ -> throw({kogen, 2, "error: invalid arguments"}) end,
    case Decoded of
        Argv when is_list(Argv), Argv =/= [] ->
            case lists:all(fun(A) -> is_binary(A) andalso A =/= <<>> andalso binary:match(A, <<0>>) =:= nomatch end, Argv) of
            true -> ok;
            false -> throw({kogen, 2, "error: invalid arguments"}) end,
            Job = #{<<"id">> => Id, <<"argv">> => Argv, <<"attempts">> => 0, <<"done">> => false,
                <<"exit_code">> => 0, <<"stdout">> => <<>>, <<"stderr">> => <<>>},
            save(Store, Jobs ++ [Job]), write(<<"queued ", Id/binary, "\n">>);
        _ -> throw({kogen, 2, "error: invalid arguments"})
    end;
dispatch(<<"status">>, _Values, Store) ->
    Jobs = load_jobs(Store),
    lists:foreach(fun(J) ->
        Id = maps:get(<<"id">>, J),
        Line = case {maps:get(<<"done">>, J), maps:get(<<"exit_code">>, J)} of
            {false, _} -> [Id, " pending\n"];
            {true, 0} -> [Id, " succeeded\n"];
            {true, Code} -> [Id, " failed ", integer_to_binary(Code), "\n"]
        end,
        io:put_chars(standard_io, Line)
    end, Jobs);
dispatch(<<"run">>, _Values, Store) ->
    Jobs = load_jobs(Store),
    {_Final, Rows} = run_jobs(Jobs, Store, [], []),
    lists:foreach(fun(Row) -> io:put_chars(standard_io, Row) end, Rows);
dispatch(_, _, _) -> throw({kogen, 2, "error: invalid arguments"}).

load_jobs(Store) ->
    Path = filename:join(Store, "state.json"),
    case file:read_file(Path) of
        {error, enoent} -> [];
        {ok, Data} -> maps:get(<<"jobs">>, json:decode(Data));
        _ -> throw({kogen, 4, "error: store failure"})
    end.
save(Store, Jobs) ->
    Temp = filename:join(Store, ".state-" ++ os:getpid() ++ ".tmp"),
    Data = json:encode(#{<<"jobs">> => Jobs}),
    case file:write_file(Temp, Data, [sync]) of
        ok -> ok = file:rename(Temp, filename:join(Store, "state.json")), sync_dir(Store);
        _ -> throw({kogen, 4, "error: store failure"})
    end.
sync_dir(Store) ->
    Port = open_port({spawn_executable, "/usr/bin/sync"}, [binary, exit_status, use_stdio, {args, ["-f", Store]}]),
    case port_wait(Port) of 0 -> ok; _ -> throw({kogen, 4, "error: store failure"}) end.

run_jobs([], _Store, Rows, Done) -> {Done, lists:reverse(Rows)};
run_jobs([Job | Rest], Store, Rows, Done) ->
    case maps:get(<<"done">>, Job) of
        true ->
            run_jobs(Rest, Store, Rows, Done ++ [Job]);
        false ->
            Attempts = maps:get(<<"attempts">>, Job) + 1,
            Started = Job#{<<"attempts">> := Attempts},
            save(Store, Done ++ [Started | Rest]),
            {Code, Stdout, Stderr} = child(maps:get(<<"argv">>, Job)),
            Complete = Started#{<<"done">> := true, <<"exit_code">> := Code, <<"stdout">> := Stdout, <<"stderr">> := Stderr},
            save(Store, Done ++ [Complete | Rest]),
            Status = if Code =:= 0 -> <<"succeeded">>; true -> <<"failed">> end,
            Row = <<"{\"id\":", (iolist_to_binary(json:encode(maps:get(<<"id">>, Job))))/binary,
                ",\"attempt\":", (integer_to_binary(Attempts))/binary, ",\"exit_code\":", (integer_to_binary(Code))/binary,
                ",\"stdout\":", (iolist_to_binary(json:encode(Stdout)))/binary,
                ",\"stderr\":", (iolist_to_binary(json:encode(Stderr)))/binary,
                ",\"status\":", (iolist_to_binary(json:encode(Status)))/binary, "}\n">>,
            run_jobs(Rest, Store, [Row | Rows], Done ++ [Complete])
    end.

child([Exe | Args]) ->
    case executable(Exe) of
        false -> {127, <<>>, <<"exec failed\n">>};
        true ->
            N = os:getpid() ++ "-" ++ integer_to_list(erlang:unique_integer([positive])),
            Out = "/tmp/kogen-out-" ++ N, Err = "/tmp/kogen-err-" ++ N,
            Script = "exec \"$@\" > \"$KOGEN_OUT\" 2> \"$KOGEN_ERR\"",
            Port = open_port({spawn_executable, "/bin/sh"}, [binary, exit_status, use_stdio,
                {args, ["-c", Script, "sh", binary_to_list(Exe) | [binary_to_list(A) || A <- Args]]},
                {env, [{"KOGEN_OUT", Out}, {"KOGEN_ERR", Err}]}]),
            Code = port_wait(Port),
            Stdout = output(Out), Stderr = output(Err), file:delete(Out), file:delete(Err),
            {Code, repair(Stdout), repair(Stderr)}
    end.
executable(B) ->
    P = case binary:match(B, <<"/">>) of nomatch -> os:find_executable(binary_to_list(B)); _ -> binary_to_list(B) end,
    case P of false -> false; _ -> case file:read_file_info(P) of {ok, I} -> (I#file_info.mode band 8#111) =/= 0; _ -> false end end.
port_wait(Port) -> receive {Port, {exit_status, Code}} -> Code; {Port, {data, _}} -> port_wait(Port) end.
output(Path) -> case file:read_file(Path) of {ok, Bin} -> Bin; _ -> <<>> end.
repair(Bin) -> repair(Bin, <<>>).
repair(<<>>, Acc) -> Acc;
repair(Bin, Acc) ->
    case unicode:characters_to_binary(Bin, utf8, utf8) of
        Valid when is_binary(Valid) -> <<Acc/binary, Valid/binary>>;
        {error, Good, Rest} -> <<_Bad, Tail/binary>> = Rest, repair(Tail, <<Acc/binary, Good/binary, 16#EF,16#BF,16#BD>>);
        {incomplete, Good, _Rest} -> <<Acc/binary, Good/binary, 16#EF,16#BF,16#BD>>
    end.
