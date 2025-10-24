"""
Small helper script to start debugpy when launched by Blender.

Usage: Run Blender with --python /path/to/tools/start_debugpy_in_blender.py

This script attempts to import debugpy and start it listening on port 5678.
It prints helpful messages to the Blender console so the developer can attach
the VS Code debugger using the existing launch.json which attaches to port 5678.
"""

import sys
import time

PORT = 5678

def main():
    try:
        import debugpy  # type: ignore  # noqa: F401  # linter: debugpy is installed in Blender's Python, not the workspace venv
    except Exception as e:
        print("debugpy is not installed in Blender's Python environment:", e)
        print("Run the VS Code task 'Install debugpy into Blender Python' to install it.")
        return

    try:
        print(f"Starting debugpy on port {PORT} and waiting for client...")
        # Listen on all interfaces to allow attaching from host
        debugpy.listen(("0.0.0.0", PORT))
        # Optionally wait for the client to attach. Set to True when you want
        # Blender to pause until the debugger is attached.
        wait_for_client = True
        if wait_for_client:
            print("Waiting for debugger to attach...")
            debugpy.wait_for_client()
            print("Debugger attached, continuing execution.")
    except Exception as e:
        print("Failed to start debugpy:", e)


if __name__ == '__main__':
    main()
