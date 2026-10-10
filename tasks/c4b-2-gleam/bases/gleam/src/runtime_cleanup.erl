-module(runtime_cleanup).
-on_load(init/0).
-export([quiesce/0]).
init() ->
    Base = filename:dirname(filename:dirname(code:which(?MODULE))),
    erlang:load_nif(filename:join([Base,"priv","runtime_cleanup"]),0).
quiesce() -> erlang:nif_error(not_loaded).
