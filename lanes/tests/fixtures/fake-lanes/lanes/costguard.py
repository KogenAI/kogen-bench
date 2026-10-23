"""Stand-in for `python3 -m lanes.costguard cells <run-dir>` on a fake remote host: fake cells spend nothing."""
import sys

if __name__ == "__main__":
    if sys.argv[1:2] != ["cells"]:
        sys.exit("usage: python3 -m lanes.costguard cells <run-dir>")
    print("{}")
