-module(workflow_os).
-on_load(init/0).

-export([
    raw_args/0,
    ensure_dir/1,
    lock_exclusive/1,
    release_lock/1,
    fsync_directory/1,
    halt/1,
    write_stderr/1
]).

init() ->
    Beam = code:which(?MODULE),
    Ebin = filename:dirname(Beam),
    Priv = filename:join(filename:dirname(Ebin), "priv"),
    erlang:load_nif(filename:join(Priv, "workflow_os_nif"), 0).

raw_args() ->
    case file:read_file("/proc/self/cmdline") of
        {ok, Bytes} ->
            Args0 = binary:split(Bytes, <<0>>, [global]),
            Args = case lists:reverse(Args0) of [<<>> | Rest] -> lists:reverse(Rest); _ -> Args0 end,
            case lists:dropwhile(fun(Arg) -> Arg =/= <<"-extra">> end, Args) of
                [<<"-extra">> | Plain] -> Plain;
                _ -> []
            end;
        {error, _} -> []
    end.

ensure_dir(Directory) when is_binary(Directory), byte_size(Directory) > 0 ->
    case filelib:ensure_dir(filename:join(Directory, <<".gleam-probe">>)) of
        ok -> {ok, nil};
        {error, _} -> {error, nil}
    end;
ensure_dir(_) ->
    {error, einval}.

lock_exclusive(_Path) -> erlang:nif_error(nif_not_loaded).
release_lock(_Lock) -> erlang:nif_error(nif_not_loaded).
fsync_directory(_Path) -> erlang:nif_error(nif_not_loaded).

halt(Code) -> erlang:halt(Code).
write_stderr(Message) -> io:put_chars(standard_error, [Message, "\n"]).
