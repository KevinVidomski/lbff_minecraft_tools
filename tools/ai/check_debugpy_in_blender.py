#!/usr/bin/env python3
"""
Diagnostic helper: check whether `debugpy` is importable from Blender's Python.

Prints sys.executable, version, sys.path, site-packages locations and whether
`debugpy` can be found/imported (and where).
"""
import sys
import pkgutil
import site

def main():
    print("PYTHON:", sys.executable)
    print("VERSION:", sys.version.splitlines()[0])
    print("\n--- sys.path ---")
    for p in sys.path:
        print(" ", p)

    print("\n--- site packages ---")
    try:
        print("getsitepackages:", site.getsitepackages())
    except Exception:
        print("getsitepackages: not available")
    try:
        print("getusersitepackages:", site.getusersitepackages())
    except Exception:
        print("getusersitepackages: not available")

    print("\n--- debugpy discovery ---")
    try:
        loader = pkgutil.find_loader('debugpy')
    except Exception as e:
        loader = None
        print("pkgutil.find_loader raised:", e)
    print("pkgutil.find_loader ->", loader)

    try:
        import debugpy
        print("import debugpy -> OK")
        print("debugpy module file:", getattr(debugpy, '__file__', '<no __file>'))
    except Exception as e:
        print("import debugpy -> FAILED:", e)


if __name__ == '__main__':
    main()
