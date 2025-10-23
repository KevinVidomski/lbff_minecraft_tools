# Contributing to LBFF

This repo contains small Blender addons. Follow these lightweight rules to make contributions easy for humans and AI assistants (Copilot, etc.).

## Addon template

- Use `addons/lbff_addon_template/__init__.py` as a starting point.
- Keep functions small, add module and function docstrings, and include type hints for public functions.
- Preserve `bl_info` metadata and the `register()` / `unregister()` pattern.

## PR checklist (required)

- [ ] Module docstring with purpose and registration contract
- [ ] Public functions have docstrings and type hints
- [ ] Example usage or a tiny test exists or is sketched
- [ ] `bl_info` metadata present and accurate
- [ ] `register()` / `unregister()` idempotent and documented

- [ ] Use `.github/PR_BODY.md` for long PR descriptions and set the PR body with:

  ```bash
  gh pr edit <pr-number> --body-file .github/PR_BODY.md
  ```

## Notes for reviewers

- Look for `# TODO: Copilot:` markers — they indicate AI-assisted stubs that need a human review.
- If the addon modifies menus, ensure `TOPBAR_MT_editor_menus.append` / `.remove` calls are paired and `LBFF_MT_main_menu` ownership is respected.

## Development tooling

We provide a small pre-commit hook that enforces the draw-callback storage rule. To enable it locally:

```powershell
# install pre-commit (once)
python -m pip install --user pre-commit

# install hooks into your git repo (run from repo root)
pre-commit install

# run hooks locally
pre-commit run --all-files
```

The hook runs `tools/check_draw_callback_storage.py` which ensures any use of `TOPBAR_MT_editor_menus.append(...)` in Python modules is accompanied by a draw-callback assignment (e.g. `MyMenu._draw_fn = draw_fn`). This prevents accidental removal of other addons' callbacks.

## Automated contributors

All AI agents MUST record themselves in `.github/AI_CONTRIBUTORS.md` before performing work in the repository on any given day. Use the format:

Agent display name — nickname: user provided nickname model: model name or "undisclosed" — date: YYYY-MM-DD
