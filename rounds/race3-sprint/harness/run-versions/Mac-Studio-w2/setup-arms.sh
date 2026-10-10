#!/bin/bash
# setup-arms.sh — fresh repo per arm from the race3 kit template (+ spec/, conformance/), with PRIVATE copy-on-write caches inside the repo
# (no writable cache is shared between arms; the agent sandbox can write them) and a repo-local .kit-env.sh that AGENTS.md sources.
R=$(cd "$(dirname "$0")" && pwd); KIT=${RACE3_KIT_DIR:-~/Scratch.noindex/race3-kit}
for L in $(cat $R/ARMS); do
  case "$R/$L" in "$R/"?*) rm -rf "$R/$L" "$R/out/$L";; esac
  cp -c -p -R $KIT/templates/$L $R/$L; cd $R/$L; git init -q; cp -R $R/inputs/spec $R/inputs/conformance . ; cp $R/TARGET.md .
  mkdir -p .kitcache; for c in cargo go-build go golangci gopls mix hex xdg config data npm bun bun-transpiler; do [ -d $KIT/cache/$c ] && cp -c -p -R $KIT/cache/$c .kitcache/$c; done; mkdir -p .kitcache/tmp
  sed "s#export RACE3_KIT=.*#export RACE3_KIT=$KIT#; /^if \[ -n \"\${BASH_SOURCE/,/^fi\$/d" $KIT/env-aids.sh | sed "s#\$RACE3_KIT/cache/#$R/$L/.kitcache/#g; s#\"\$RACE3_KIT/cache/#\"$R/$L/.kitcache/#g" > .kit-env.sh
  printf '# Same build environment for every language; ./kogen is prebuilt, and the scorer passes no toolchain or cache vars to it.\nexport RACE3_KIT=%s\n' "$KIT" | cat - .kit-env.sh > .kit-env.tmp && mv .kit-env.tmp .kit-env.sh
  sed -i '' "s#\. \"$KIT/env-aids.sh\"#. ./.kit-env.sh#g" AGENTS.md
  printf 'target/\n_build/\ndeps/\nnode_modules/\n.cache/\nbuild/\n.kitcache/\n' >> .gitignore
done; echo arms-ready
