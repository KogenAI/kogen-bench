-module(approval_io).
-on_load(load_nif/0).
-export([not_implemented/0, prepare_shutdown/0, prepare_shutdown_nif/0]).

load_nif() ->
    BeamDir = filename:dirname(code:which(?MODULE)),
    erlang:load_nif(filename:join(BeamDir, "approval_nif"), 0).

prepare_shutdown_nif() -> erlang:nif_error(nif_not_loaded).

prepare_shutdown() -> prepare_shutdown_nif().

not_implemented() ->
    io:put_chars(standard_error, <<"{\"error\":{\"code\":\"NOT_IMPLEMENTED\",\"message\":\"not implemented\"}}\n">>),
    erlang:halt(70).
