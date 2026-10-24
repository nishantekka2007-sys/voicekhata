"""Gemma transaction extraction via a local Ollama-compatible chat endpoint."""
from __future__ import annotations
import json
import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma4:e4b")
VALID_TYPES = {"credit_sale", "payment_received", "cash_expense", "unknown"}

SYSTEM_PROMPT = """You extract ledger transactions from a vendor's spoken or typed note.
Return ONLY one JSON object with keys: transaction_type, customer_name, amount, description, needs_clarification, clarification_reason.
transaction_type must be credit_sale, payment_received, cash_expense, or unknown.
Use amount as a positive number only when explicitly clear; otherwise null. Use null for missing customer_name.
A credit sale means goods were sold on credit and the customer owes money. A payment_received means a customer paid money back. A cash_expense is money spent by the vendor.
Never invent missing details. If the intent or amount is ambiguous, set transaction_type to unknown or needs_clarification to true.
Descriptions should be short. Output valid JSON, no markdown."""


def extract_transaction(text: str, *, model: str | None = None, timeout: int = 90) -> dict:
    text = text.strip()
    if not text:
        raise ValueError("Enter or transcribe a transaction first.")
    response = requests.post(OLLAMA_URL, json={
        "model": model or GEMMA_MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
        "stream": False,
        "format": "json",
    }, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    raw = payload.get("message", {}).get("content", "")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemma returned invalid JSON. Try rephrasing the transaction.") from exc
    kind = data.get("transaction_type", "unknown")
    if kind not in VALID_TYPES:
        kind = "unknown"
    amount = data.get("amount")
    try:
        amount = float(amount) if amount is not None else None
        if amount is not None and amount <= 0:
            amount = None
    except (ValueError, TypeError):
        amount = None
    customer = data.get("customer_name")
    return {
        "transaction_type": kind,
        "customer_name": str(customer).strip() if customer else "",
        "amount": amount,
        "description": str(data.get("description") or "").strip(),
        "needs_clarification": bool(data.get("needs_clarification", False)) or kind == "unknown" or amount is None,
        "clarification_reason": str(data.get("clarification_reason") or "").strip(),
    }
