## .github/PR_BODY.md — AI submission template and rules

## Purpose

This file is a template and short guide for automated agents (AIs/bots) and humans submitting long-form text to GitHub (PR bodies and extended commit messages). Use it as the canonical source when constructing multi-paragraph content so GitHub UI renders it correctly.

## Rules summary (what to follow)

- Always provide real newlines. Do NOT include literal escape sequences like `\n` or `\n\n` in the text body. GitHub renders real newlines; escaped sequences will appear verbatim in the UI.
- Use Markdown for structure: headings (##), lists (- or \*), fenced code blocks for examples, and blank lines between paragraphs.
- For programmatic edits, write the formatted Markdown into a file (for example `.github/PR_BODY.md`) and use `gh pr edit --body-file <file>` or the REST API body field. This preserves newlines and avoids escaping issues.
- When producing long commit messages, place the full Markdown body in the commit message body (after the subject line and a blank line). Use `git commit -F <file>` to ensure Git reads the file contents literally.
- Avoid embedding triple-backtick fences inside single-line strings. If you must include a code fence in the text, ensure you write it as its own line(s) in the file.

## Template (fill in the sections)

Title: <Short, one-line subject>

## Summary

<A short paragraph summarizing the change. Keep it 1–3 sentences.>

## Highlights

- <Bullet: notable change or file touched>
- <Bullet: tests added/updated>
- <Bullet: CI/lint changes>

## Changelog

- <Bullet: short, imperative change description>
- <Bullet: short, imperative change description>

Example (use this file as-is with `gh pr edit --body-file .github/PR_BODY.md`):

Refactor addons, add template/tests/linter/CI, and enforce draw-callback storage.

## Summary

This PR refactors the LBFF addons to a lightweight module pattern, adds a small addon template and a pytest smoke test, enforces a draw-callback storage pattern across addons, and wires an AST-based linter and pre-commit checks into CI.

## Highlights

- Addon refactor: `lbff_minecraft_importer`, `lbff_gaffer`, `lbff_all_in_one` and a new `lbff_addon_template`
- Tests: `tests/test_addon_template.py` (fakes `bpy`) — passes locally
- Linter: `tools/check_draw_callback_storage.py` enforces draw-callback storage and passes across codebase
- Pre-commit: local hooks added and configured to always run (`.pre-commit-config.yaml`)
- AI provenance: `.github/AI_CONTRIBUTORS.csv` normalized to raw CSV and docs added in `.github/AI_CONTRIBUTORS.md` / `CONTRIBUTING.md`

## Changelog

- Normalize `.github/AI_CONTRIBUTORS.csv` to raw CSV so validators and pre-commit work
- Add/adjust pre-commit hooks and docs in `CONTRIBUTING.md`
- Add addon template, tests, and AST linter for draw-callback storage
- Update `.pre-commit-config.yaml` to always run local hooks
  Refactor addons, add template/tests/linter/CI, and enforce draw-callback storage.

## Summary

This PR refactors the LBFF addons to a lightweight module pattern, adds a small addon template and a pytest smoke test, enforces a draw-callback storage pattern across addons, and wires an AST-based linter and pre-commit checks into CI.

## Highlights

- Addon refactor: `lbff_minecraft_importer`, `lbff_gaffer`, `lbff_all_in_one` and a new `lbff_addon_template`
- Tests: `tests/test_addon_template.py` (fakes `bpy`) — passes locally
- Linter: `tools/check_draw_callback_storage.py` enforces draw-callback storage and passes across codebase
- Pre-commit: local hooks added and configured to always run (`.pre-commit-config.yaml`)
- AI provenance: `.github/AI_CONTRIBUTORS.csv` normalized to raw CSV and docs added in `.github/AI_CONTRIBUTORS.md` / `CONTRIBUTING.md`

## Changelog

- Normalize `.github/AI_CONTRIBUTORS.csv` to raw CSV so validators and pre-commit work
- Add/adjust pre-commit hooks and docs in `CONTRIBUTING.md`
- Add addon template, tests, and AST linter for draw-callback storage
- Update `.pre-commit-config.yaml` to always run local hooks
