#!/usr/bin/env python3
"""Check that TOPBAR_MT_editor_menus.append calls store the draw callback.

This linter looks for calls like:
    bpy.types.TOPBAR_MT_editor_menus.append(draw_fn)

and ensures the same module contains an assignment to a draw-callback attribute
on a menu class, e.g. `MyMenu._draw_fn = draw_fn` or `MyMenu._menu_draw = menu_draw`.

Exit code 0 when all checks pass, non-zero otherwise.
"""
import ast
import sys
from pathlib import Path


def module_has_draw_assignment(tree: ast.AST) -> bool:
    """Return True if module AST contains an assignment to an attribute with 'draw' in the name."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
                    if isinstance(target.attr, str) and "draw" in target.attr:
                        return True
    return False


def find_topbar_appends(tree: ast.AST):
    """Yield (lineno, col) for append calls on TOPBAR_MT_editor_menus."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            func = node.func
            if func.attr == "append":
                # check the value is an attribute chain ending with TOPBAR_MT_editor_menus
                value = func.value
                # value could be Name/Attribute; we just search for the final attr name
                if isinstance(value, ast.Attribute) and getattr(value, "attr", "") == "TOPBAR_MT_editor_menus":
                    yield node.lineno, node.col_offset


def check_file(path: Path):
    src = path.read_text(encoding="utf8")
    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        print(f"[ERROR] Could not parse {path}")
        return False

    appends = list(find_topbar_appends(tree))
    if not appends:
        return True

    has_assign = module_has_draw_assignment(tree)
    if not has_assign:
        print(f"[LINT] {path}: TOPBAR_MT_editor_menus.append found but no draw-callback assignment in module")
        return False
    return True


def main():
    repo_root = Path(__file__).resolve().parents[1]
    failures = []
    for py in repo_root.rglob("*.py"):
        # skip virtualenv, .git, tests, and tools self
        if any(part in (".venv", ".git", "__pycache__") for part in py.parts):
            continue
        if py.match("tests/**"):
            continue
        if "tools" in py.parts and py.name == Path(__file__).name:
            continue
        ok = check_file(py)
        if not ok:
            failures.append(py)

    if failures:
        print(f"\n[LINT] {len(failures)} file(s) failed draw-callback storage check")
        sys.exit(1)
    print("[LINT] draw-callback storage check passed")


if __name__ == "__main__":
    main()
