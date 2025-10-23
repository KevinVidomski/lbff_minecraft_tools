Refactor addons, add template/tests/linter/CI, and enforce draw-callback storage.

Summary

This PR refactors the LBFF addons into a lightweight, modular layout, adds a small addon template and a pytest smoke test that runs without Blender, enforces a draw-callback storage pattern across addons, and wires an AST-based linter plus pre-commit checks into CI.

Highlights

- Refactor: `lbff_minecraft_importer`, `lbff_gaffer`, `lbff_all_in_one` reorganized for clarity and testability
- Template & tests: added `addons/lbff_addon_template` and `tests/test_addon_template.py` (fake `bpy`) — tests pass locally
- Linter: added `tools/check_draw_callback_storage.py` to enforce storing draw callbacks on menu classes and removing the exact callable
- Pre-commit & CI: local hooks and `.github/workflows/pytest.yml` run linter and tests; pre-commit configured to always run local hooks
- AI provenance: normalized `.github/AI_CONTRIBUTORS.csv` to raw CSV and added docs for recording automated agents

Changelog

- Normalize `.github/AI_CONTRIBUTORS.csv` to raw CSV so validators and pre-commit work
- Add local pre-commit hooks and adjust `.pre-commit-config.yaml` to always run the local scripts
- Add addon template, pytest smoke test, and AST linter for draw-callback storage
- Update documentation (`CONTRIBUTING.md`, `.github/PR_BODY.md`, `.github/AI_CONTRIBUTORS.md`) to explain workflows and provenance
