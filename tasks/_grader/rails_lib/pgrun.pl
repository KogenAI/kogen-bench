#!/usr/bin/perl
# pgrun.pl SECONDS cmd args...  run cmd in its own process group; on timeout kill the whole group (Rails parallel workers included). exit 124 on timeout.
use POSIX;
my $t = shift @ARGV;
my $pid = fork();
die "fork: $!" unless defined $pid;
if (!$pid) { setpgid(0, 0); exec @ARGV or die "exec: $!"; }
setpgid($pid, $pid);
$SIG{ALRM} = sub { kill "TERM", -$pid; sleep 2; kill "KILL", -$pid; print STDERR "PGRUN_TIMEOUT after ${t}s\n"; exit 124; };
alarm $t;
waitpid($pid, 0);
my $st = $?;
kill "KILL", -$pid;  # stragglers
exit(($st & 127) ? 128 + ($st & 127) : ($st >> 8));
