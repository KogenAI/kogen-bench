"""Compatibility import; all replay/reporting policy is shared."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'shared'))
from replay import Replay, report
