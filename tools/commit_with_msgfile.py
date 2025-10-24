#!/usr/bin/env python3
"""Helper to commit using a temporary message file.

Usage examples:
  python tools/commit_with_msgfile.py -m "My long commit message" -- -a
  python tools/commit_with_msgfile.py --message-file ./mymsg.txt -- path/to/file.py

This script writes the provided message (or stdin) to a temporary file and runs
`git commit -F <tempfile>` with any extra args forwarded. This avoids issues with
shell quoting for long or complex commit messages and follows the project's
preference to always save long commit descriptions to a file.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Commit using a temporary message file")
    grp = p.add_mutually_exclusive_group(required=False)
    grp.add_argument('-m', '--message', help='Commit message string')
    grp.add_argument('--message-file', help='Path to an existing file to use as the commit message')
    p.add_argument('git_args', nargs=argparse.REMAINDER, help='Additional args to pass to git commit (e.g. -a, -- path)')
    args = p.parse_args()

    if args.message_file:
        msg_path = Path(args.message_file)
        if not msg_path.exists():
            print(f'Error: message file {msg_path} does not exist', file=sys.stderr)
            return 2
        commit_file = msg_path
        use_temp = False
    else:
        # If message provided use it, otherwise read stdin (allow piping)
        if args.message is None:
            if sys.stdin.isatty():
                print('Enter commit message, end with EOF (Ctrl-D):')
            message = sys.stdin.read()
        else:
            message = args.message

        # write to a temporary file
        tmp = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        tmp.write(message)
        tmp.flush()
        tmp.close()
        commit_file = Path(tmp.name)
        use_temp = True

    try:
        cmd = ['git', 'commit', '-F', str(commit_file)] + args.git_args
        print('Running:', ' '.join(cmd))
        proc = subprocess.run(cmd)
        return proc.returncode
    finally:
        # remove the temporary file if we created one
        if 'use_temp' in locals() and use_temp:
            try:
                commit_file.unlink()
            except Exception:
                pass


if __name__ == '__main__':
    raise SystemExit(main())
