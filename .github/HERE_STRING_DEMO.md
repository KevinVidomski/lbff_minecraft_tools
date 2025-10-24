This file demonstrates why embedding PowerShell here-strings or multi-line scripts directly in `tasks.json` is problematic.

Reason:
- `tasks.json` is parsed as strict JSON by some tools (and by our test suite).
- JSON does not support JavaScript-style `//` comments or PowerShell here-strings like `@' ... '@`.
- Embedding a multi-line here-string directly in the `args` array will break JSON parsing and cause tools/tests to fail.

Example (invalid - do NOT put this directly into `tasks.json`):

```powershell
@'
# Prompt for Blender python.exe if not set
if (-not $env:BLENDER_PYTHON) {
  $input = Read-Host 'Enter full path to Blender python.exe'
}
'@
```

Recommended alternatives:
- Keep `tasks.json` strict JSON (single-line strings). For long scripts, write the script to a separate `.ps1` file and reference it from the task.
- Use a single-string PowerShell command (escaped and newline-embedded) inside `tasks.json`.

This demo branch previously included a commented header in `tasks.json` to illustrate the parse error; that header was moved here so the repository tests remain green while preserving the demonstration content for reviewers.
