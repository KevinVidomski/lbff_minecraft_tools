# Automated contributors

AI contributor rule (mandatory):

- Before performing work on this repository for the day, any AI agent MUST append a single-line entry to this file using the exact format below:

  Agent display name — model: model name or "undisclosed" — date: YYYY-MM-DD

- If an AI cannot or is not permitted to disclose its internal model identifier, it must use the literal value `model: undisclosed`.

Notes:

- Ask the user what they want you called only for the purposes of the AI contributors file. Agents MUST be truthful. Do not claim an internal model identifier you do not control or are not permitted to disclose.
- Human maintainers may require additional provenance (e.g., a PR comment or external audit log) for sensitive changes.

Unverified user assertions (2025-10-22):

- User reported: "You are GPT5-mini" — recorded as an unverified assertion; agents must not self-identify based on unverified user claims.
