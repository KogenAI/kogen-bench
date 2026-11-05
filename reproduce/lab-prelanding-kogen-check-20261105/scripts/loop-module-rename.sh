#!/bin/bash
# loop-module-rename.sh <cli-dir>: after sync-kogen-loop.sh, when the vendored copy's module path (third_party/kogen-loop/go.mod)
# differs from the path cli/go.mod uses for it, rename it mechanically in kogen: the replace's left side, the require, and import
# paths in cli/'s own Go files (never the vendored copy). Main ruling 4 Nov (L-MODULE-PATH): a pin consequence, made in the pin
# commit. Prints "renamed <old> -> <new> in <n> file(s)" when it changed anything; prints nothing and exits 0 otherwise.
# The renamed Go files are gofmt'd: a new path sorts elsewhere in an import block (5 Nov: 15 files left unsorted made the
# adoption go step's gofmt -l check red with no output). Exits 1 if gofmt is missing or fails.
set -u; c=$1; v=$c/third_party/kogen-loop/go.mod; g=$c/go.mod
[ -f "$v" ] && [ -f "$g" ] || exit 0
new=$(awk '$1=="module"{print $2; exit}' "$v")
old=$(awk '{l=$0; sub(/^[[:space:]]+/,"",l); sub(/^replace[[:space:]]+/,"",l); n=split(l,a,/[[:space:]]+/); for(i=1;i<n;i++) if(a[i]=="=>" && a[i+1] ~ /third_party\/kogen-loop\/?$/) print a[1]}' "$g" | head -1)
[ -n "$new" ] && [ -n "$old" ] && [ "$new" != "$old" ] || exit 0
OLD=$old NEW=$new perl -pi -e 's/^(\s*(?:replace\s+)?)\Q$ENV{OLD}\E(\s+(?:=>|v\S+))/$1$ENV{NEW}$2/; s/^(require\s+)\Q$ENV{OLD}\E(\s)/$1$ENV{NEW}$2/' "$g"
n=0; fs=(); while IFS= read -r f; do
  grep -q "\"$old[/\"]" "$f" || continue
  OLD=$old NEW=$new perl -pi -e 's/"\Q$ENV{OLD}\E(\/|")/"$ENV{NEW}$1/g' "$f"; n=$((n+1)); fs+=("$f")
done < <(find "$c" -name '*.go' -not -path "$c/third_party/*")
PATH=$PATH:$HOME/.local/share/mise/installs/go/1.27.2/bin
[ $n = 0 ] || gofmt -w "${fs[@]}" || { echo "gofmt of the renamed files failed" >&2; exit 1; }
echo "renamed $old -> $new in $((n+1)) file(s)"
