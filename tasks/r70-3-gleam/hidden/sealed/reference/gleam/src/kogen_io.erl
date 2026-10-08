-module(kogen_io).
-export([args/0, read/1, write/1, fail/2, matches/2, position/2, execute/1]).

args() -> [unicode:characters_to_binary(Arg) || Arg <- init:get_plain_arguments()].
read(Path) ->
    Result = case Path of none -> stdin(); {some, <<"-">>} -> stdin(); {some, File} -> file:read_file(File) end,
    case Result of {ok, Bytes} -> {ok, Bytes}; _ -> {error, unreadable} end.
stdin() -> io:setopts(standard_io, [binary, {encoding, latin1}]), chunks([]).
chunks(Acc) -> case io:get_chars(standard_io, "", 65536) of eof -> {ok, iolist_to_binary(lists:reverse(Acc))}; {error, Reason} -> {error, Reason}; Bytes -> chunks([Bytes | Acc]) end.
write(Text) -> io:put_chars(standard_io, Text), nil.
fail(Code, Message) -> io:put_chars(standard_error, [Message, <<"\n">>]), erlang:halt(Code).
matches(Pattern, Text) -> re:run(Text, Pattern, [{capture, none}]) =:= match.
position(Text, Needle) -> case binary:match(Text, Needle) of {At, _} -> At; nomatch -> -1 end.

execute(Args) ->
    case parse_args(Args) of
        error -> {error, {failure, 2, <<"error: invalid arguments">>}};
        {ok, Opts} ->
            try run(Opts) of
                {Text, Input, Output} ->
                    write_usage(maps:get(usage, Opts), Input, Output),
                    {ok, <<Text/binary, "\n">>}
            catch _:_ -> {error, {failure, 5, <<"error: request failed">>}} end
    end.

parse_args([<<"model">> | Args]) when length(Args) =:= 8 ->
    Pairs = pairs(Args, []),
    Keys = [<<"--url">>, <<"--prompt">>, <<"--idle-timeout-ms">>, <<"--usage-file">>],
    case Pairs of
        error -> error;
        _ ->
            KeyList = [K || {K, _} <- Pairs],
            case lists:sort(KeyList) =:= lists:sort(Keys) of
                false -> error;
                true ->
                    Map = maps:from_list(Pairs), Url = maps:get(<<"--url">>, Map), Prompt = maps:get(<<"--prompt">>, Map),
                    RawTimeout = maps:get(<<"--idle-timeout-ms">>, Map), Usage = maps:get(<<"--usage-file">>, Map),
                    case decimal(RawTimeout) andalso byte_size(Usage) > 0 andalso valid_url(Url) of
                        true -> try binary_to_integer(RawTimeout) of N when N >= 1, N =< 60000 -> {ok, #{url => Url, prompt => Prompt, timeout => N, usage => Usage}}; _ -> error catch _:_ -> error end;
                        false -> error
                    end
            end
    end;
parse_args(_) -> error.

pairs([], Acc) -> lists:reverse(Acc);
pairs([Key, Value | Rest], Acc) when Key =:= <<"--url">>; Key =:= <<"--prompt">>; Key =:= <<"--idle-timeout-ms">>; Key =:= <<"--usage-file">> ->
    case lists:keymember(Key, 1, Acc) of true -> error; false -> pairs(Rest, [{Key, Value} | Acc]) end;
pairs(_, _) -> error.
decimal(<<>>) -> false;
decimal(Bin) -> lists:all(fun(C) -> C >= $0 andalso C =< $9 end, binary_to_list(Bin)).
valid_url(Url) -> case uri_string:parse(Url) of #{scheme := <<"http">>, host := Host} when byte_size(Host) > 0 -> true; _ -> false end.

run(Opts) ->
    application:ensure_all_started(inets),
    Body = json:encode(#{<<"prompt">> => maps:get(prompt, Opts)}),
    request(Opts, Body, 0).
request(Opts, Body, Attempt) ->
    Url = maps:get(url, Opts), Timeout = maps:get(timeout, Opts),
    Headers = [{"Content-Type", "application/json"}, {"Accept", "text/event-stream"}],
    Req = {binary_to_list(Url), Headers, "application/json", Body},
    HttpOpts = [{timeout, infinity}, {connect_timeout, Timeout}, {autoredirect, false}],
    ReqOpts = [{sync, false}, {stream, self}],
    case httpc:request(post, Req, HttpOpts, ReqOpts) of
        {ok, RequestId} -> await_response(RequestId, Timeout, Opts, Body, Attempt);
        {error, _} -> retry(Opts, Body, Attempt)
    end.
await_response(RequestId, Timeout, Opts, Body, Attempt) ->
    receive
        {http, {RequestId, stream_start, _Headers}} ->
            case receive_body(RequestId, Timeout, []) of {ok, Response} -> parse_sse(Response); {error, _} -> retry(Opts, Body, Attempt) end;
        {http, {RequestId, {{_Version, Status, _Reason}, _Headers, Response}}} when Status >= 200, Status =< 299 -> parse_sse(Response);
        {http, {RequestId, {{_Version, Status, _Reason}, _Headers, _Response}}} when Status >= 500, Status =< 599 -> retry(Opts, Body, Attempt);
        {http, {RequestId, {error, _Reason}}} -> retry(Opts, Body, Attempt);
        {http, {RequestId, _Response}} -> throw(http_status)
    after Timeout -> httpc:cancel_request(RequestId), retry(Opts, Body, Attempt)
    end.
receive_body(RequestId, Timeout, Chunks) ->
    receive
        {http, {RequestId, stream, Chunk}} -> receive_body(RequestId, Timeout, [Chunk | Chunks]);
        {http, {RequestId, stream_end, _Headers}} -> {ok, iolist_to_binary(lists:reverse(Chunks))};
        {http, {RequestId, {error, Reason}}} -> {error, Reason}
    after Timeout -> httpc:cancel_request(RequestId), {error, idle_timeout}
    end.
retry(Opts, Body, 0) -> request(Opts, Body, 1);
retry(_, _, _) -> throw(retries_exhausted).

parse_sse(Bytes) ->
    case unicode:characters_to_binary(Bytes, utf8, utf8) of
        Valid when is_binary(Valid) -> parse_lines(binary:split(Valid, <<"\n">>, [global]), <<>>, none, [], false);
        _ -> throw(bad_utf8)
    end.
parse_lines([], _Text, _Usage, _Fields, _Done) -> throw(incomplete_stream);
parse_lines(_Lines, Text, Usage, _Fields, true) ->
    case Usage of {Input, Output} -> {Text, Input, Output}; _ -> throw(missing_usage) end;
parse_lines([Raw | Rest], Text, Usage, Fields, _Done) ->
    Line = strip_cr(Raw),
    if Line =:= <<>> andalso Fields =/= [] ->
        Data = join(lists:reverse(Fields), <<"\n">>),
        case Data of
            <<"[DONE]">> -> parse_lines(Rest, Text, Usage, [], true);
            _ ->
                Push = fun(Key, Value, Acc) -> [{Key, Value} | Acc] end,
                Finish = fun(Pairs, Acc) -> {maps:from_list(lists:reverse(Pairs)), Acc} end,
                {Obj, _Acc, <<>>} = json:decode(Data, none, #{object_push => Push, object_finish => Finish}),
                case is_map(Obj) of false -> throw(bad_event); true -> ok end,
                case maps:get(<<"type">>, Obj, undefined) of
                    <<"text">> -> case maps:get(<<"text">>, Obj, undefined) of V when is_binary(V) -> parse_lines(Rest, <<Text/binary, V/binary>>, Usage, [], false); _ -> throw(bad_text) end;
                    <<"usage">> ->
                        I = maps:get(<<"input_tokens">>, Obj, invalid), O = maps:get(<<"output_tokens">>, Obj, invalid),
                        case count(I) andalso count(O) of true -> parse_lines(Rest, Text, {I, O}, [], false); false -> throw(bad_usage) end;
                    _ -> parse_lines(Rest, Text, Usage, [], false)
                end
        end;
    Line =:= <<>> -> parse_lines(Rest, Text, Usage, [], false);
    true -> parse_nonblank(Line, Rest, Text, Usage, Fields)
    end.
parse_nonblank(<<":", _/binary>>, Rest, Text, Usage, Fields) -> parse_lines(Rest, Text, Usage, Fields, false);
parse_nonblank(<<"data:", Value0/binary>>, Rest, Text, Usage, Fields) ->
    Value = case Value0 of <<" ", Tail/binary>> -> Tail; _ -> Value0 end,
    parse_lines(Rest, Text, Usage, [Value | Fields], false);
parse_nonblank(_, Rest, Text, Usage, Fields) -> parse_lines(Rest, Text, Usage, Fields, false).
strip_cr(<<>>) -> <<>>;
strip_cr(Bin) -> case Bin of <<Rest:(byte_size(Bin)-1)/binary, "\r">> -> Rest; _ -> Bin end.
join([], _) -> <<>>;
join([H], _) -> H;
join([H | T], Sep) -> <<H/binary, Sep/binary, (join(T, Sep))/binary>>.
count(N) when is_integer(N) -> N >= 0 andalso N =< 9007199254740991;
count(N) when is_float(N) -> N >= 0 andalso N =< 9007199254740991 andalso N == trunc(N);
count(_) -> false.

write_usage(Path, Input, Output) ->
    Dir = filename:dirname(binary_to_list(Path)), ok = filelib:ensure_dir(filename:join(Dir, "placeholder")),
    Temp = filename:join(Dir, ".kogen-usage-" ++ integer_to_list(erlang:unique_integer([positive]))),
    Bytes = iolist_to_binary(io_lib:format("{\"input_tokens\":~B,\"output_tokens\":~B}\n", [integer_count(Input), integer_count(Output)])),
    ok = file:write_file(Temp, Bytes, [exclusive, binary]), ok = file:rename(Temp, binary_to_list(Path)).

integer_count(N) when is_float(N) -> trunc(N);
integer_count(N) -> N.
