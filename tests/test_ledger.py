from voicekhata.ledger import add_transaction, customer_balances, daily_summary, initialize_db, transaction_history


def test_balance_sales_minus_payments_expenses_excluded(tmp_path):
    db = tmp_path / "test.db"
    initialize_db(db)
    add_transaction(customer_name="Ramesh", transaction_type="credit_sale", amount=500, description="rice", db_path=db)
    add_transaction(customer_name="Ramesh", transaction_type="payment_received", amount=200, description="part payment", db_path=db)
    add_transaction(customer_name=None, transaction_type="cash_expense", amount=50, description="tea", db_path=db)
    assert customer_balances(db) == [{"customer": "Ramesh", "balance": 300.0}]
    assert daily_summary(db)["expenses"] == 50.0


def test_rejects_missing_customer_for_sale(tmp_path):
    db = tmp_path / "test.db"
    initialize_db(db)
    try:
        add_transaction(customer_name=None, transaction_type="credit_sale", amount=100, db_path=db)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "customer name" in str(exc).lower()


def test_rejects_unknown_type_and_nonpositive_amount(tmp_path):
    db = tmp_path / "test.db"
    initialize_db(db)
    for kind, amount in [("unknown", 20), ("cash_expense", 0)]:
        try:
            add_transaction(customer_name=None, transaction_type=kind, amount=amount, db_path=db)
            assert False, "Expected ValueError"
        except ValueError:
            pass


def test_history_contains_saved_transactions(tmp_path):
    db = tmp_path / "test.db"
    initialize_db(db)
    add_transaction(customer_name="Suresh", transaction_type="credit_sale", amount=120, db_path=db)
    rows = transaction_history(db_path=db)
    assert len(rows) == 1
    assert rows[0]["customer"] == "Suresh"
