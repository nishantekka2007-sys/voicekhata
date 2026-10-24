# Contributing to VoiceKhata

Thank you for your interest in contributing! The project is in early development, so discussion, documentation, tests, bug reports, and small focused pull requests are all useful.

## Ways to contribute

- Report a reproducible bug or suggest an improvement through GitHub Issues.
- Improve documentation or setup instructions.
- Add or improve tests for Hindi, English, and Hinglish transaction examples.
- Improve speech transcription, transaction extraction, validation, or the ledger UI.
- Help with accessibility, privacy, and mobile usability.

## Before starting

1. Check existing issues and pull requests to avoid duplicate work.
2. For a substantial change, open an issue first to discuss the approach.
3. Keep changes focused and explain the problem they solve.
4. Never include real customer financial information, private audio, credentials, API keys, or local database files.

## Suggested workflow

1. Fork the repository if you are not a repository collaborator.
2. Create a branch from `main`, for example `fix/transaction-validation` or `docs/setup-guide`.
3. Make your changes and add or update tests where appropriate.
4. Run the relevant tests and describe the results honestly.
5. Commit your changes with a clear message.
6. Open a pull request against `main`, linking the relevant issue if one exists.
7. Respond to review feedback and update the pull request as needed.

Repository collaborators should also use focused branches and pull requests so changes can be reviewed and contributions remain easy to understand.

## Pull request checklist

- [ ] The purpose and scope of the change are explained.
- [ ] Tests were added or updated where appropriate.
- [ ] Documentation was updated if behavior or setup changed.
- [ ] No secrets, private recordings, real customer data, local databases, or model weights were added.
- [ ] Third-party code, datasets, and model terms have been checked where relevant.
- [ ] Any limitations or tests not run are clearly disclosed.

## Development principles

- Validate model output before it reaches the ledger.
- Require explicit confirmation before saving a transaction.
- Calculate balances with deterministic application logic.
- Prefer clear error messages over silently guessing.
- Keep changes understandable and testable.

## Code of conduct

Be respectful, constructive, and welcoming. Critique ideas and code rather than people. Harassment, discrimination, personal attacks, and disruptive behavior are not acceptable. Project maintainers may remove content or close participation that violates these expectations.

## License

By submitting a contribution, you agree that your contribution will be distributed under the repository's MIT License, subject to applicable rights and obligations. Please do not submit code or assets you do not have the right to contribute.
