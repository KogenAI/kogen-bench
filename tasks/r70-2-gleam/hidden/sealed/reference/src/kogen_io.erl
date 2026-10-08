-module(kogen_io).
-include_lib("kernel/include/file.hrl").
-export([args/0, read/1, write/1, fail/2, matches/2, position/2, supervise/1, halt/1]).

args() -> [unicode:characters_to_binary(A) || A <- init:get_plain_arguments()].
read(P) -> R = case P of none -> stdin(); {some, <<"-">>} -> stdin(); {some, F} -> file:read_file(F) end,
    case R of {ok, B} -> ascii(B, 1, 1, B); _ -> {error, unreadable} end.
stdin() -> io:setopts(standard_io,[binary,{encoding,latin1}]), chunks([]).
chunks(A) -> case io:get_chars(standard_io,"",65536) of eof->{ok,iolist_to_binary(lists:reverse(A))}; {error,R}->{error,R}; B->chunks([B|A]) end.
ascii(<<>>,_,_,B)->{ok,B};
ascii(<<C,_/binary>>,L,P,_) when C>127->{error,{not_ascii,L,P}};
ascii(<<10,R/binary>>,L,_,B)->ascii(R,L+1,1,B);
ascii(<<_,R/binary>>,L,P,B)->ascii(R,L,P+1,B).
write(T)->io:put_chars(standard_error,T),nil.
fail(C,M)->io:put_chars(standard_error,[M,<<"\n">>]),erlang:halt(C).
halt(C)->erlang:halt(C).
matches(P,T)->re:run(T,P,[{capture,none}])=:=match.
position(T,N)->case binary:match(T,N) of {At,_}->At;nomatch->-1 end.

supervise(A)->case parse(A) of error->{error,{failure,2,<<"error: invalid arguments">>}}; {ok,T,G,C,Rest}->run(T,G,C,Rest) end.
parse([<<"supervise">>,<<"--timeout-ms">>,T,<<"--grace-ms">>,G,<<"--">>,C|R]) when byte_size(C)>0 ->
    case {millis(T),millis(G)} of {{ok,TM},{ok,GM}}->{ok,TM,GM,C,R};_->error end;
parse(_)->error.
millis(B)->case re:run(B,<<"^[0-9]+$">>,[{capture,none}]) of match->try binary_to_integer(B) of N when N>=1,N=<60000->{ok,N};_->error catch _:_ -> error end;_->error end.

run(T,G,C,Args)->case executable(C) of true->run_started(T,G,C,Args);false->{error,{failure,127,<<"error: cannot start command">>}} end.
executable(C)->S=binary_to_list(C), P=case lists:member($/,S) of true->S;false->os:find_executable(S) end,
    case P of false->false;undefined->false;Path->case file:read_file_info(Path) of {ok,#file_info{type=regular,mode=Mode}}->(Mode band 8#111)=/=0;_->false end end.
run_started(T,G,C,Args)->
    GroupFile=filename:join("/tmp","kogen-pg-"++os:getpid()++"-"++integer_to_list(erlang:unique_integer([positive]))),
    ErrFile=filename:join("/tmp","kogen-err-"++os:getpid()++"-"++integer_to_list(erlang:unique_integer([positive]))),
    Launch="exec /usr/bin/setsid --wait /bin/sh -c 'exec 2>/dev/null; printf \"%s\" \"$$\" > \"$1\"; shift; Err=$1; shift; exec </dev/null; \"$@\" 2>\"$Err\" & Child=$!; wait \"$Child\" 2>/dev/null; exit $?' kogen \"$@\" 2>/dev/null",
    P=open_port({spawn_executable,"/bin/sh"},[binary,exit_status,use_stdio,{args,["-c",Launch,"kogen",GroupFile,ErrFile,binary_to_list(C)|[binary_to_list(X)||X<-Args]]}]),
    PG=group_id(GroupFile,erlang:monotonic_time(millisecond)+1000),file:delete(GroupFile),D=erlang:monotonic_time(millisecond)+T,
    case poll(P,PG,D) of
      {done,Code}->emit_stderr(ErrFile),{ok,{Code,line("exited",Code,false,false)}};
      timeout->signal(PG,"TERM"), grace(P,PG,erlang:monotonic_time(millisecond)+G), K=live(PG),
        case K of true->signal(PG,"KILL"),dead(P,PG);false->ok end,
        _=exit_code(P),emit_stderr(ErrFile),{ok,{124,line("timeout",124,true,K)}}
    end.

group_id(F,D)->case file:read_file(F) of {ok,B}->case string:to_integer(binary_to_list(B)) of {N,[]}->N;_->erlang:error(bad_process_group) end;_->case erlang:monotonic_time(millisecond)>=D of true->erlang:error(process_group_timeout);false->receive after 1->group_id(F,D) end end end.
emit_stderr(F)->case file:read_file(F) of {ok,B}->io:put_chars(standard_error,B);_->ok end,file:delete(F).

poll(P,PG,D)->
    case live(PG) of
      false->{done,exit_code(P)};
      true->case erlang:monotonic_time(millisecond)>=D of
        true->timeout;
        false->receive {P,{data,B}}->io:put_chars(standard_io,B),poll(P,PG,D); {P,{exit_status,C}}->put({kogen_exit,P},C),poll(P,PG,D) after 5->poll(P,PG,D) end
      end
    end.
grace(P,PG,D)->case erlang:monotonic_time(millisecond)<D of
    true->receive {P,{data,B}}->io:put_chars(standard_io,B); {P,{exit_status,C}}->put({kogen_exit,P},C) after 5->ok end,grace(P,PG,D);
    false->ok end.
dead(P,PG)->case live(PG) of true->receive {P,{data,B}}->io:put_chars(standard_io,B); {P,{exit_status,C}}->put({kogen_exit,P},C) after 5->ok end,dead(P,PG);false->ok end.
exit_code(P)->case get({kogen_exit,P}) of undefined->receive {P,{data,B}}->io:put_chars(standard_io,B),exit_code(P); {P,{exit_status,C}}->put({kogen_exit,P},C),C end; C->C end.
signal(PG,S)->P=open_port({spawn_executable,"/bin/kill"},[binary,exit_status,use_stdio,stderr_to_stdout,{args,["-"++S,"--","-"++integer_to_list(PG)]}]),wait_signal(P).
wait_signal(P)->receive {P,{exit_status,_}}->ok; {P,{data,_}}->wait_signal(P) after 1000->ok end.

live(PG)->case file:list_dir("/proc") of {ok,Es}->lists:any(fun(E)->entry_live(E,PG) end,Es);_->false end.
entry_live(E,PG)->case string:to_integer(E) of {_,[]}->case file:read_file(filename:join(["/proc",E,"stat"])) of
    {ok,S}->case string:split(binary_to_list(S),") ",trailing) of [_Prefix,Tail]->case string:tokens(Tail," ") of [State,_Parent,Group|_]->State=/="Z" andalso State=/="X" andalso list_to_integer(Group)=:=PG;_->false end;_->false end;
    _->false end;_->false end.
line(K,C,T,S)->iolist_to_binary(io_lib:format("status=~s exit_code=~B term_sent=~s kill_sent=~s reaped=1~n",[K,C,bool(T),bool(S)])).
bool(true)->"true";bool(false)->"false".
