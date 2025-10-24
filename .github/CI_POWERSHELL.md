CI: PowerShell (pwsh) on Linux runners
=====================================

Why
---
Some repository tests run a PowerShell script (`tools/install_debugpy.ps1`) in a dry-run. Most Linux CI runners do not have Windows PowerShell installed by default. To exercise the PowerShell path in CI (or to run the script with `pwsh`) add a small setup step to the workflow.

Options
-------
1) Use the system package (APT) on Ubuntu runners (install pwsh):

   ```yaml
   - name: Install PowerShell (Ubuntu)
     run: |
       sudo apt-get update
       sudo apt-get install -y wget apt-transport-https software-properties-common
       wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb
       sudo dpkg -i packages-microsoft-prod.deb
       sudo apt-get update
       sudo apt-get install -y powershell
   ```

2) Use the official setup action (recommended for brevity and cross-distro support):

   ```yaml
   - name: Setup PowerShell
     uses: PowerShell/PowerShell@v1
     with:
       version: '7.4'
   ```

   (If an `actions/setup-pwsh` action exists later, prefer that. The point is to ensure `pwsh` is on PATH.)

What to add to workflow
-----------------------
- Add one of the steps above before tests run. Then CI will exercise the `pwsh` branch of `test_vscode_tasks.py` instead of the static validation.

Notes
-----
- The test still supports static validation when no `pwsh` is available; installing PowerShell in CI only adds additional coverage.
- Installing `pwsh` increases job runtime by a short amount (~10-30s depending on image and network).

Example (full jobs snippet)
--------------------------

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Setup PowerShell
        uses: PowerShell/PowerShell@v1
        with:
          version: '7.4'
      - name: Install deps
        run: python -m pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest -q
```

If you want, I can open a follow-up PR that updates the repository workflows to include a PowerShell setup step.
