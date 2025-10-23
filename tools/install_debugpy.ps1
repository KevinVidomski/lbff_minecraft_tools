## Installer script for debugpy in Blender's Python
# Usage: powershell -NoProfile -File "<workspace>\tools\install_debugpy.ps1"

# Prompt for Blender python.exe if not set
if (-not $env:BLENDER_PYTHON) {
  $input = Read-Host 'Enter full path to Blender python.exe [D:/Program Files/Blender/4.5/python/bin/python.exe]:'
  if ([string]::IsNullOrWhiteSpace($input)) {
    $env:BLENDER_PYTHON = 'D:/Program Files/Blender/4.5/python/bin/python.exe'
  } else {
    $env:BLENDER_PYTHON = $input
  }
}

# Check if the python.exe exists
if (-not (Test-Path $env:BLENDER_PYTHON)) {
  Write-Host ""
  Write-Host 'ERROR: The specified Blender python.exe was not found.' -ForegroundColor Red
  Write-Host 'Please check your Blender installation directory and try again.' -ForegroundColor Yellow
  Write-Host 'Tip: Open Blender, go to Scripting workspace, and run: import sys; print(sys.executable)'
  exit 1
}

# Try to install debugpy
try {
  & "$env:BLENDER_PYTHON" -m ensurepip
  & "$env:BLENDER_PYTHON" -m pip install --upgrade pip
  & "$env:BLENDER_PYTHON" -m pip install debugpy
} catch {
  Write-Host ""
  Write-Host 'ERROR: Failed to run python commands in Blender''s Python.' -ForegroundColor Red
  Write-Host 'Make sure Blender is installed correctly and you have permission to run its python.exe.' -ForegroundColor Yellow
  exit 1
}
