import json
import os
import shutil
import subprocess
import pytest

tasks_path = os.path.join(os.path.dirname(__file__), '../.vscode/tasks.json')

def load_tasks():
    with open(tasks_path, encoding='utf-8') as f:
        return json.load(f)

def test_tasks_json_valid():
    # Should load as valid JSON
    data = load_tasks()
    assert isinstance(data, dict)
    assert 'tasks' in data
    assert isinstance(data['tasks'], list)

def test_debugpy_install_task_present():
    data = load_tasks()
    install = [t for t in data['tasks'] if t.get('label') == 'Install debugpy into Blender Python']
    assert install, 'Install debugpy task not found'
    task = install[0]
    assert task['type'] == 'shell'
    assert task['command'] == 'powershell'
    args = task['args']
    assert isinstance(args, list) and len(args) >= 3
    # Two supported forms:
    #  - inline: [-NoProfile, -Command, <script string>]
    #  - file:   [-NoProfile, -File, <path-to-ps1>]
    script = args[2]
    if args[1].lower() == '-file' or script.lower().endswith('.ps1'):
        # load the referenced file and inspect its contents
        script_path = os.path.join(os.path.dirname(__file__), '..', script.replace('${workspaceFolder}', '').lstrip('/\\'))
        script_path = os.path.normpath(script_path)
        with open(script_path, encoding='utf-8') as sf:
            script_text = sf.read()
    else:
        script_text = script

    # Check for prompt, path check, and debugpy install
    assert 'Read-Host' in script_text
    assert 'Test-Path' in script_text
    assert 'pip install debugpy' in script_text
    assert 'ERROR:' in script_text
    assert 'import sys; print(sys.executable)' in script_text

def test_blender_start_task_present():
    data = load_tasks()
    start = [t for t in data['tasks'] if t.get('label') == 'Start Blender with debugpy startup script']
    assert start, 'Start Blender with debugpy startup script task not found'
    task = start[0]
    assert task['type'] == 'shell'
    assert 'BLENDER_EXE' in task['command']
    assert 'start_debugpy_in_blender.py' in task['command']
    assert 'envFile' in task.get('options', {})

def test_markdownlint_task_present():
    data = load_tasks()
    lint = [t for t in data['tasks'] if t.get('type') == 'markdownlint']
    assert lint, 'markdownlint task not found'
    task = lint[0]
    assert '$markdownlint' in ''.join(task.get('problemMatcher', []))


def test_debugpy_install_task_dry_run():
    """
    Run the PowerShell script in a subprocess with a dummy path, check for expected prompt and error, but avoid real changes.
    """
    # If PowerShell (Windows PowerShell) or pwsh (PowerShell Core) is available, run a dry-run
    # invocation; otherwise fall back to a static validation of the script contents so the test
    # works on Linux CI where PowerShell is not installed.
    pwsh_exec = shutil.which("powershell") or shutil.which("pwsh")
    data = load_tasks()
    install = [t for t in data['tasks'] if t.get('label') == 'Install debugpy into Blender Python']
    assert install, 'Install debugpy task not found'
    task = install[0]
    args = task['args']
    script = args[2]
    # Use a dummy path that does not exist
    env = os.environ.copy()
    env['BLENDER_PYTHON'] = 'Z:/not/a/real/path/python.exe'
    # Run the script in PowerShell, capture output
    if not pwsh_exec:
        # Static validation on platforms without PowerShell: ensure the script contains the
        # expected checks and messages (prompt, path test, pip install, error message, tip).
        if args[1].lower() == '-file' or script.lower().endswith('.ps1'):
            script_path = os.path.join(os.path.dirname(__file__), '..', script.replace('${workspaceFolder}', '').lstrip('/\\'))
            script_path = os.path.normpath(script_path)
            with open(script_path, encoding='utf-8') as sf:
                script_text = sf.read()
        else:
            script_text = script

        assert 'Read-Host' in script_text or 'read-host' in script_text.lower()
        assert 'Test-Path' in script_text or 'test-path' in script_text.lower()
        assert 'pip install debugpy' in script_text
        assert 'ERROR:' in script_text
        assert 'import sys; print(sys.executable)' in script_text
        return

    # PowerShell exists: run the script (either -File or -Command) in a subprocess and assert
    # it fails with the expected error when BLENDER_PYTHON points to a non-existent path.
    if args[1].lower() == '-file' or script.lower().endswith('.ps1'):
        ps_path = script.replace('${workspaceFolder}', os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        ps_command = [pwsh_exec, "-NoProfile", "-File", ps_path]
    else:
        ps_command = [pwsh_exec, "-NoProfile", "-Command", script]

    proc = subprocess.run(ps_command, env=env, capture_output=True, text=True, timeout=20)
    # Should exit with code 1 (error)
    assert proc.returncode == 1
    # Should print the error about not found
    assert 'ERROR: The specified Blender python.exe was not found.' in proc.stdout or proc.stderr
    # Should print the tip
    assert 'import sys; print(sys.executable)' in proc.stdout or proc.stderr
