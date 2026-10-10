#!/usr/bin/env python3
import subprocess
raise SystemExit(subprocess.run(['mix','test'],cwd='app').returncode)
