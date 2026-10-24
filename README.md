# VoiceKhata

A Gemma 4-powered, voice-first digital ledger for Indian micro-vendors.

## MVP status

This is an early prototype. The first end-to-end path is **transaction text → Gemma extraction → editable review → explicit confirmation → SQLite → deterministic balance**. The interface includes an audio recording widget, but transcription is not wired up yet. We will connect a verified Gemma 4 audio runtime or an optional speech-to-text fallback next.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) or a compatible local inference server
- A Gemma 4 model tag supported by your installed runtime

## Run locally

    git clone https://github.com/nishantekka2007-sys/voicekhata.git
    cd voicekhata
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

Check your runtime's current Gemma 4 model tags, pull an audio-capable E2B/E4B model if available, then start the local model server. The default tag is configurable:

    export GEMMA_MODEL='gemma4:e4b'
    streamlit run app.py

If your installed runtime uses a different tag, set GEMMA_MODEL to that exact tag. The parser uses the local Ollama-compatible /api/chat endpoint by default; override it with OLLAMA_URL if needed.

## Test ledger logic

    pytest -q

## Safety principles

- AI output is a draft, not a source of truth.
- The vendor must review and explicitly confirm before a transaction is saved.
- Python/SQLite calculates balances; the language model does not do arithmetic.
- Ambiguous transactions must be clarified, not guessed.
- Use synthetic demo data. Never commit private customer records, recordings, credentials, local databases, or model weights.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The repository code is MIT-licensed; model weights and third-party dependencies may have separate terms.
