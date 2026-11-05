#!/bin/sh
# R-20261103-X-V1 residual fixture: detached servers started by node, perl, go and python
# launchers (environment cleared, new session, inherited descriptors closed, launcher exits),
# then a kill-group zombie probe. Exit status = the probe's.
P=$1
D=$(dirname "$0")
: > "$P"
node -e 'const {spawn}=require("child_process"),fs=require("fs");const c=spawn("/bin/sleep",["300"],{detached:true,stdio:"ignore",env:{}});fs.appendFileSync(process.argv[1],c.pid+" node\n");c.unref();' "$P"
perl -e 'use POSIX qw(setsid); my $f=shift; my $pid=fork(); if(!defined $pid){exit 1} if($pid==0){ setsid(); open(STDIN,"<","/dev/null"); open(STDOUT,">","/dev/null"); open(STDERR,">","/dev/null"); POSIX::close($_) for 3..255; %ENV=(); exec("/bin/sleep","300"); POSIX::_exit(127);} open(my $h,">>",$f) or exit 1; print $h "$pid perl\n"; close $h; exit 0;' "$P"
"$D/golaunch/golaunch" "$P"
python3 -c 'import subprocess,sys; p=subprocess.Popen(["/bin/sleep","300"],env={},start_new_session=True,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); open(sys.argv[1],"a").write("%d python\n"%p.pid)' "$P"
echo "launched: $(wc -l < "$P") servers"
python3 "$D/zprobe.py"
rc=$?
echo "fixture done"
exit $rc
