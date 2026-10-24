# VoiceKhata

**A voice-first digital ledger for Indian micro-vendors.**

VoiceKhata is an open-source project exploring how small shopkeepers and vendors can record customer credit, payments, and shop expenses using natural speech instead of typing every transaction.

> **Project status:** Early development. Features described as planned are not yet guaranteed to be implemented.

## Problem

Small vendors often track customer credit in paper notebooks or manually typed apps. VoiceKhata aims to make transaction recording faster through a simple voice-first workflow.

## Planned MVP

- Record or upload a short audio clip.
- Transcribe speech with an appropriate speech-recognition model.
- Use an instruction-tuned Gemma model to extract structured transaction details.
- Let the vendor review and confirm the proposed transaction before saving.
- Store confirmed transactions in SQLite.
- Show customer history, outstanding balances, and a daily summary.
- Provide typed input as a fallback.

## Intended technology

- Python and Streamlit
- Gemma through a compatible inference runtime such as Ollama
- Whisper / faster-whisper for speech-to-text
- SQLite
- Git and GitHub

Exact model versions and their applicable terms will be documented as implementation decisions are finalized. The repository's MIT license applies to this project's code, not automatically to third-party models, weights, or dependencies.

## Data integrity and privacy

- Validate AI output before saving it.
- Require explicit user confirmation for transactions.
- Calculate balances with deterministic application logic, not generated arithmetic.
- Ask for clarification when a transaction is ambiguous or incomplete.
- Use synthetic demo data only; do not commit real customer financial records.
- Never commit secrets, private recordings, local databases, or downloaded model weights.

## Project status

Installation and usage instructions will be added once the corresponding application code and dependencies are verified.

## Contributing

Contributions from the founding team and the wider open-source community are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

This project is licensed under the [MIT License](LICENSE), except where a file or third-party component states otherwise.
