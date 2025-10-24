# Blender Debug Attach (VS Code)

This guide explains how to set up and attach the VS Code debugger to Blender using debugpy.

## 1. Configure Blender paths

Create or edit the `.env` file in your workspace root:

```env
BLENDER_PYTHON=D:/Program Files/Blender/4.5/python/bin/python.exe
BLENDER_EXE=D:/Program Files/Blender/blender.exe
```

Update the paths to match your Blender installation.

## 2. Install debugpy into Blender's Python

In VS Code, open the Command Palette and run the task:

- **Tasks: Run Task** → `Install debugpy into Blender Python`

If you have not set `BLENDER_PYTHON` in your `.env`, you will be prompted for the path.

Note: The installer script now lives in `tools/install_debugpy.ps1`. The VS Code task runs this script with `powershell -File` so you can edit and test the installer directly from `tools/`.

## 3. Start Blender with debugpy

Run the task:

- **Tasks: Run Task** → `Start Blender with debugpy startup script`

This will launch Blender and run the helper script that starts debugpy listening on port 5678.

## E2E (End to End) check script and configurable timeout

For automated tests we provide an E2E-friendly startup script at
`tools/ai/start_debugpy_e2e_check.py`. Unlike the regular startup script
which optionally waits for a debugger, the E2E script starts debugpy listening
and sleeps for a short period so a test harness can attach and then continue.

Configuration

- The sleep timeout (seconds) is read from the environment variable
  `BLENDER_DEBUGPY_E2E_TIMEOUT`. For convenience this repository's example
  `.env` file contains `BLENDER_DEBUGPY_E2E_TIMEOUT=12`.
- You can also override the timeout per-launch with a CLI argument:

```ps1
blender --python tools/ai/start_debugpy_e2e_check.py -- --timeout 5
```

Notes

- The `--` separates Blender's `--python` argument from the script's own
  arguments.
- Use the E2E script in CI to programmatically verify the debugpy listener
  is accepting connections on port 5678 without blocking indefinitely.

## 4. Attach the VS Code debugger

Use the provided `.vscode/launch.json` configuration:

- **Run & Debug** → `Python: Attach to Blender debugpy`

This will connect to Blender's Python process. Once attached, you can set breakpoints in your addon code.

---

**Troubleshooting:**

- If you see an error about `debugpy` not found, make sure you have installed it into Blender's Python (not your workspace venv).
  If you get a connection error, check that Blender is running and the debugpy script is active (see Blender's system console for messages).
