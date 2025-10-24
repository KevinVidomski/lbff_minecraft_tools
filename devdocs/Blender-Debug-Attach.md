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

This will launch Blender and run the helper script that starts debugpy listening on port 5678.

## Editor setup for linting and Intellisense

This repository includes lightweight type stubs for `debugpy` so your editor
and linters (Pylance/pyright/pylint) can resolve `import debugpy` even when
debugpy is only installed into Blender's embedded Python. The stubs live in
`stubs/debugpy` and provide minimal signatures used by the startup script.

If you're using VS Code the workspace settings are configured to find the
stubs automatically (`.vscode/settings.json`). After pulling these changes
reload the window (Developer: Reload Window) so the Python language server
picks up the updated `python.analysis.extraPaths`.

If you prefer not to use the bundled stubs, you can point your editor directly
at your Blender installation's site-packages directory instead (for example,
`D:\Program Files\Blender Foundation\Blender 4.5\4.5\python\Lib\site-packages`).

## 4. Attach the VS Code debugger

Use the provided `.vscode/launch.json` configuration:

This will connect to Blender's Python process. Once attached, you can set breakpoints in your addon code.

---

**Troubleshooting:**

- If you see an error about `debugpy` not found, make sure you have installed it into Blender's Python (not your workspace venv).
  If you get a connection error, check that Blender is running and the debugpy script is active (see Blender's system console for messages).
