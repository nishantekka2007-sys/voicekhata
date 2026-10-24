# Project status

VoiceKhata is at the repository setup and planning stage.

## AI-first design

Gemma 4 is the primary model. First, evaluate an audio-capable Gemma 4 instruction-tuned variant (E2B or E4B) for speech understanding and transaction extraction. These variants support audio input, but compatibility with the chosen local inference runtime must be tested. See the [official model card](https://ai.google.dev/gemma/docs/core/model_card_4).

If a direct audio workflow is not reliable in the time available, use faster-whisper as an optional speech-to-text fallback and send the resulting text to Gemma 4. Keep the initial stack small.

## MVP goals

1. Capture audio in a Streamlit interface, with typed text as a fallback.
2. Evaluate Gemma 4 native audio input first.
3. Extract structured transaction fields using Gemma 4.
4. Validate and display a reviewable transaction preview.
5. Save only confirmed transactions to SQLite.
6. Calculate customer balances with deterministic logic.
7. Test normal, ambiguous, incomplete, and failed-input cases.

## Not yet promised

Unless implementation and tests are present in the repository, the following should be treated as future work: production deployment, multi-user authentication, cloud synchronization, payment processing, automatic reminders, and support for every Indian language or dialect.

## Demo data

Use synthetic names and amounts only. Do not store real shopkeeper or customer financial records in the repository.
