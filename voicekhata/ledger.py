"""SQLite persistence and deterministic ledger calculations."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_DB = Path("data/voicekhata.db")
TRANSACTION_TYPES = {"credit_sale", "payment_received", "cash_expense"}


def connect(db_path: str | Path = DEFAULT_DB) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db(db_path: str | Path = DEFAULT_DB) -> None:
    with connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE COLLATE NOCASE
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('credit_sale','payment_received','cash_expense')),
            amount REAL NOT NULL CHECK(amount > 0),
            description TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            confirmed INTEGER NOT NULL DEFAULT 1 CHECK(confirmed = 1),
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )""")


def add_transaction(*, customer_name: str | None, transaction_type: str, amount: float,
                    description: str = "", db_path: str | Path = DEFAULT_DB) -> int:
    """Persist only a user-confirmed, validated transaction. Returns transaction ID."""
    if transaction_type not in TRANSACTION_TYPES:
        raise ValueError("Unsupported transaction type")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    if transaction_type in {"credit_sale", "payment_received"} and not (customer_name or "").strip():
        raise ValueError("A customer name is required for sales and payments")

    with connect(db_path) as conn:
        customer_id = None
        if customer_name and customer_name.strip():
            name = customer_name.strip()
            conn.execute("INSERT OR IGNORE INTO customers(name) VALUES (?)", (name,))
            row = conn.execute("SELECT id FROM customers WHERE name = ? COLLATE NOCASE", (name,)).fetchone()
            customer_id = int(row["id"])
        cur = conn.execute(
            "INSERT INTO transactions(customer_id, transaction_type, amount, description, confirmed) VALUES (?, ?, ?, ?, 1)",
            (customer_id, transaction_type, float(amount), description.strip()),
        )
        return int(cur.lastrowid)


def customer_balances(db_path: str | Path = DEFAULT_DB) -> list[dict[str, Any]]:
    """Outstanding balance = credit sales minus payments received; expenses are excluded."""
    with connect(db_path) as conn:
        rows = conn.execute("""SELECT c.name,
            COALESCE(SUM(CASE WHEN t.transaction_type='credit_sale' THEN t.amount
                              WHEN t.transaction_type='payment_received' THEN -t.amount
                              ELSE 0 END), 0) AS balance
            FROM customers c LEFT JOIN transactions t ON t.customer_id=c.id AND t.confirmed=1
            GROUP BY c.id, c.name ORDER BY c.name COLLATE NOCASE""").fetchall()
        return [{"customer": row["name"], "balance": round(float(row["balance"]), 2)} for row in rows]


def transaction_history(limit: int = 100, db_path: str | Path = DEFAULT_DB) -> list[dict[str, Any]]:
    with connect(db_path) as conn:
        rows = conn.execute("""SELECT t.id, c.name AS customer, t.transaction_type, t.amount,
            t.description, t.created_at FROM transactions t LEFT JOIN customers c ON c.id=t.customer_id
            WHERE t.confirmed=1 ORDER BY t.id DESC LIMIT ?""", (limit,)).fetchall()
        return [dict(row) for row in rows]


def daily_summary(db_path: str | Path = DEFAULT_DB) -> dict[str, float]:
    with connect(db_path) as conn:
        row = conn.execute("""SELECT
            COALESCE(SUM(CASE WHEN transaction_type='credit_sale' THEN amount ELSE 0 END),0) AS credit_sales,
            COALESCE(SUM(CASE WHEN transaction_type='payment_received' THEN amount ELSE 0 END),0) AS payments,
            COALESCE(SUM(CASE WHEN transaction_type='cash_expense' THEN amount ELSE 0 END),0) AS expenses
            FROM transactions WHERE confirmed=1 AND date(created_at)=date('now','localtime')""").fetchone()
        return {key: round(float(row[key]), 2) for key in ("credit_sales", "payments", "expenses")}
