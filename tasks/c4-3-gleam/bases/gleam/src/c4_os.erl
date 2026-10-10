-module(c4_os).
-on_load(init/0).
-export([prctl/5,waitpid/2,posix_spawn/8,kill/2,getpid/0,getpgid/1,setpgid/2,
         watch_signal/1,signal_received/1,pipe/0,read/2,write/2,close/1,realpath/1]).
init() -> erlang:load_nif(filename:join(code:priv_dir(c4_supervisor), "sys_nif"), 0).
prctl(_,_,_,_,_) -> erlang:nif_error(not_loaded).
waitpid(_,_) -> erlang:nif_error(not_loaded).
posix_spawn(_,_,_,_,_,_,_,_) -> erlang:nif_error(not_loaded).
kill(_,_) -> erlang:nif_error(not_loaded).
getpid() -> erlang:nif_error(not_loaded).
getpgid(_) -> erlang:nif_error(not_loaded).
setpgid(_,_) -> erlang:nif_error(not_loaded).
watch_signal(_) -> erlang:nif_error(not_loaded).
signal_received(_) -> erlang:nif_error(not_loaded).
pipe() -> erlang:nif_error(not_loaded).
read(_,_) -> erlang:nif_error(not_loaded).
write(_,_) -> erlang:nif_error(not_loaded).
close(_) -> erlang:nif_error(not_loaded).
realpath(_) -> erlang:nif_error(not_loaded).
