"""
E2E check variant of the Blender startup script for debugpy.

This script is intended for automated/e2e tests. It starts debugpy listening
on the standard port and sleeps for a short, configurable period instead of
blocking indefinitely waiting for a debugger. That makes it safe to launch
from CI or a short-lived test harness which will attach and then exit.

Usage: run with Blender's Python or via `blender --python <this-file>`.
"""
import time
import sys

PORT = 5678
SLEEP_SECONDS = 12

def main():
    try:
        import debugpy  # type: ignore
    except Exception as e:
        print("debugpy is not installed in Blender's Python environment:", e)
        return 1

    try:
        print(f"E2E: Starting debugpy on port {PORT} (will sleep {SLEEP_SECONDS}s)")
        debugpy.listen(("0.0.0.0", PORT))
        # Do not wait for client; sleep briefly so tests can attach then exit.
        time.sleep(SLEEP_SECONDS)
        print("E2E: Done sleeping, exiting")
        return 0
    except Exception as e:
        print("E2E: Failed to start debugpy:", e)
        return 2


if __name__ == '__main__':
    sys.exit(main())
