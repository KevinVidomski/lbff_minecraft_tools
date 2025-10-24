"""
E2E check variant of the Blender startup script for debugpy.

This script is intended for automated/e2e tests. It starts debugpy listening
on the standard port and sleeps for a short, configurable period instead of
blocking indefinitely waiting for a debugger. That makes it safe to launch
from CI or a short-lived test harness which will attach and then exit.

Usage: run with Blender's Python or via `blender --python <this-file>`.
"""
import argparse
import os
import sys
import time

PORT = 5678


def _get_timeout(cli_timeout: int | None = None) -> int:
    """Determine the timeout (seconds) to sleep for the e2e check.

    Order of precedence:
    1. CLI argument (if passed)
    2. Environment variable BLENDER_DEBUGPY_E2E_TIMEOUT (if set)
    3. Default: 12 seconds
    """
    if cli_timeout is not None:
        return cli_timeout
    env_val = os.environ.get('BLENDER_DEBUGPY_E2E_TIMEOUT')
    if env_val:
        try:
            return int(env_val)
        except ValueError:
            print(f"WARNING: BLENDER_DEBUGPY_E2E_TIMEOUT='{env_val}' is not an int; falling back to default")
    return 12


def main() -> int:
    parser = argparse.ArgumentParser(description='E2E debugpy startup check for Blender')
    parser.add_argument('--timeout', type=int, help='seconds to sleep while debugpy listens')
    args = parser.parse_args()

    timeout = _get_timeout(args.timeout)

    try:
        import debugpy  # type: ignore
    except Exception as e:
        print("debugpy is not installed in Blender's Python environment:", e)
        return 1

    try:
        print(f"E2E: Starting debugpy on port {PORT} (will sleep {timeout}s)")
        debugpy.listen(("0.0.0.0", PORT))
        # Do not wait for client; sleep briefly so tests can attach then exit.
        time.sleep(timeout)
        print("E2E: Done sleeping, exiting")
        return 0
    except Exception as e:
        print("E2E: Failed to start debugpy:", e)
        return 2


if __name__ == '__main__':
    sys.exit(main())
