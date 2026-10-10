"""Location-only replay of one failing evaluation or final failing transition.

The shared reporter adds no helper arguments, results, or state diagnostics.
Native Quint/Apalache diagnostics remain the checker's responsibility.
"""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('fv_shared_replay',Path(__file__).resolve().parents[1]/'shared/replay.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
Replay,report,map_trace=module.Replay,module.report,module.map_trace
