# Using VS Code with Blender (Windows)

This short guide shows a modern workflow for developing Blender add-ons with Visual Studio Code on Windows. It assumes you will install Blender under `D:\Program Files\Blender` and that you are using the latest Blender release.

Overview

- Use Blender's bundled Python runtime for running and debugging add-ons (runtime parity).

- Use a repository-local virtual environment (`.venv`) for linting, testing, and editor features.

- Use `debugpy` inside Blender to allow VS Code to attach and debug running code.

Steps

1. Install Blender

- Download from [Blender.org](https://www.blender.org/download) and install to `D:\Program Files\Blender`.

2. Prepare a project venv for development (editor tooling)

Open PowerShell in the repository root and run:

```powershell
# Create venv
python -m venv .venv

# Activate venv
. .venv\Scripts\Activate.ps1

# Install tooling
pip install --upgrade pip
pip install black pytest debugpy pycodestyle
```

3. Install debugpy into Blender's Python (so Blender can accept debugger connections)

Run these commands in PowerShell. Replace `<BLENDER_VERSION>` with the installed version folder (for example `4.1`):

```powershell
$blenderPython = "D:\Program Files\Blender\<BLENDER_VERSION>\python\bin\python.exe"
& $blenderPython -m ensurepip
& $blenderPython -m pip install --upgrade pip
& $blenderPython -m pip install debugpy
```

4. Start Blender and run debugpy in the Blender process

Inside Blender's Text Editor create and run a tiny snippet to start debugpy listening:

```python
import debugpy
debugpy.listen(('localhost', 5678))
print('debugpy listening on 5678')
# debugpy.wait_for_client()  # optionally block until VS Code attaches
```

5. Attach from VS Code

- Use the provided `.vscode/launch.json` attach configuration (port 5678) to attach the debugger.
- Set breakpoints and run code inside Blender; VS Code will stop at breakpoints.

Notes

- Using the same Python interpreter in VS Code as Blender can be attempted, but it may complicate tooling. The recommended approach is to use a local `.venv` for editor features and install debugpy into Blender's bundled Python runtime for debugging.
- For autocomplete stubs, you can download community stubs or the Blender API stubs and add them to `D:/autocomplete/<BLENDER_VERSION>` and point `python.analysis.extraPaths` in workspace settings.

If you want, I can create a small Blender startup script that automatically runs debugpy on Blender launch, or add a `.vscode/tasks.json` to automate the attach/start sequence.
