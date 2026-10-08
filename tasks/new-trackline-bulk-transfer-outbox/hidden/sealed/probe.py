import subprocess,sys
from pathlib import Path
s=Path(__file__).parent
sys.exit(subprocess.call(["mix","run",str(s/"probe.exs")],cwd=sys.argv[1]))
