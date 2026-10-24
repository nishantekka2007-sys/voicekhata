# Contributing to VoiceKhata

Thank you for considering a contribution! The project is in early development, so bug reports, documentation, tests, and small focused pull requests are welcome.

## Ways to contribute

- Report a reproducible bug or propose an improvement through GitHub Issues.
- Improve documentation and setup instructions.
- Add tests for Hindi, English, and Hinglish transaction examples.
- Improve transcription, transaction extraction, validation, ledger UI, accessibility, or mobile usability.

## Before starting

1. Check existing issues and pull requests to avoid duplicated effort.
2. Open an issue first for substantial changes.
3. Keep changes focused and explain the problem they solve.
4. Never include real customer financial data, private audio, credentials, API keys, local databases, or downloaded model weights.

## Workflow

1. Fork the repository if you are not a repository collaborator.
2. Create a focused branch from `main`, such as `fix/transaction-validation` or `docs/setup-guide`.
3. Make your changes and add or update tests where appropriate.
4. Run relevant tests and report results honestly.
5. Commit with a clear message.
6. Open a pull request against `main`, linking a related issue where applicable.
7. Respond to review feedback.

Repository collaborators should also use focused branches and pull requests so changes can be reviewed and contributions remain easy to understand.

## Pull request checklist

- [ ] The purpose and scope are explained.
- [ ] Tests were added or updated where appropriate.
- [ ] Documentation was updated if setup or behavior changed.
- [ ] No secrets, private recordings, real customer data, local databases, or model weights were added.
- [ ] Third-party code, data, and model terms were checked where relevant.
- [ ] Limitations and tests not run are disclosed.

## Development principles

- Validate model output before it reaches the ledger.
- Require explicit confirmation before saving transactions.
- Calculate balances with deterministic application logic.
- Ask for clarification instead of silently guessing.

## Code of conduct

Be respectful, constructive, and welcoming. Critique ideas and code rather than people. Harassment, discrimination, personal attacks, and disruptive behavior are not acceptable.

## License

By submitting a contribution, you agree that your contribution will be distributed under the repository's MIT License, subject to applicable rights and obligations. Do not submit code or assets you do not have the right to contribute.
