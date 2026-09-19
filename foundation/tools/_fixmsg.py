"""_fixmsg.py - one-off msg-filter for `git filter-branch`.

ASCII-only on purpose: all non-ASCII text lives in _goodmsg.txt, so this script
cannot itself be mis-decoded by a shell or by Python's default source encoding.

Match rule (ASCII fingerprint, no Chinese literals needed):
  subject starts with "chore:" and the body mentions "MiB" and "git_snapshot"
  -> that is commit 15b116f, whose message was double-encoded by the old
     Get-Content(ANSI) round-trip. Replace it wholesale.

Anything else passes through byte-for-byte.
"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GOOD = os.path.join(HERE, "_goodmsg.txt")

raw = sys.stdin.buffer.read().decode("utf-8", "replace")
lines = raw.splitlines()
subject = lines[0] if lines else ""
out = raw

if subject.startswith("chore:") and "MiB" in raw and "git_snapshot" in raw:
    with open(GOOD, "rb") as fh:
        out = fh.read().decode("utf-8")
    sys.stderr.write("_fixmsg: replaced message for %r\n" % subject[:40])

sys.stdout.buffer.write(out.encode("utf-8"))
