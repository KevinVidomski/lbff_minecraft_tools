# PR body template — AI submission rules

## Purpose

This file is the canonical template and short guide for automated agents (AIs/bots) and humans submitting long-form text to GitHub (PR bodies and extended commit messages). Use it to ensure multi-paragraph content renders correctly in the GitHub UI.

## Rules (short)

- Always write real newlines. Do NOT include literal `\n` or escaped newline sequences. Escaped sequences appear verbatim in the UI.
- Use Markdown with ATX headings ("#" / "##"), blank lines between paragraphs, and lists for readable structure.
- For programmatic updates: write the Markdown into a file and use `gh pr edit --body-file <file>` or call the REST API with the raw body; this preserves newlines and avoids escaping.
- For long commit messages: put the full Markdown body after the subject line and a blank line, and use `git commit -F <file>` so Git reads the file literally.
- Avoid embedding code-fence markers inside single-line JSON/string values; write fences as their own lines in the file.

## Template

Subject: <Short, one-line subject>

## Summary

<A short paragraph summarizing the change (1–3 sentences).>

## Highlights

- <Bullet: notable change or file touched>
- <Bullet: tests added/updated>
- <Bullet: CI/lint changes>

## Changelog

- <Bullet: short, imperative change description>
- <Bullet: short, imperative change description>

## How to use (commands)

Use this file as the PR body (keeps newlines intact):

```bash
gh pr edit <pr-number> --body-file .github/PR_BODY.md
```

Create a commit using this file as the full commit body:

```bash
git add <files>
git commit -F .github/PR_BODY.md
```

Create a commit with a separate subject file and body file (POSIX example):

```bash
printf "%s\n\n" "Subject line" > /tmp/msg
cat .github/PR_BODY.md >> /tmp/msg
git commit -F /tmp/msg
```

(On Windows PowerShell you can achieve the same by creating a file with the subject then appending the body file.)

## Example

Refactor addons, add template/tests/linter/CI, and enforce draw-callback storage.

### Example: Summary

This PR refactors the LBFF addons to a lightweight module pattern, adds a small addon template and a pytest smoke test, enforces a draw-callback storage pattern across addons, and wires an AST-based linter and pre-commit checks into CI.

### Example: Highlights

- Addon refactor: `lbff_minecraft_importer`, `lbff_gaffer`, `lbff_all_in_one`, and a new `lbff_addon_template`
- Tests: `tests/test_addon_template.py` (fakes `bpy`) — passes locally
- Linter: `tools/check_draw_callback_storage.py` enforces draw-callback storage and passes across codebase
- Pre-commit: local hooks added and configured to always run (`.pre-commit-config.yaml`)
- AI provenance: `.github/AI_CONTRIBUTORS.csv` normalized to raw CSV and docs added in `.github/AI_CONTRIBUTORS.md` / `CONTRIBUTING.md`

### Example: Changelog

- Normalize `.github/AI_CONTRIBUTORS.csv` to raw CSV so validators and pre-commit work
- Add/adjust pre-commit hooks and docs in `CONTRIBUTING.md`
- Add addon template, tests, and AST linter for draw-callback storage
- Update `.pre-commit-config.yaml` to always run local hooks
