"""VoiceKhata Streamlit app."""
from __future__ import annotations
import os
import streamlit as st
from voicekhata.ledger import add_transaction, customer_balances, daily_summary, initialize_db, transaction_history
from voicekhata.parser import extract_transaction

DB_PATH = os.getenv("VOICEKHATA_DB", "data/voicekhata.db")
st.set_page_config(page_title="VoiceKhata", page_icon="🧾", layout="wide")
initialize_db(DB_PATH)
st.title("🧾 VoiceKhata")
st.caption("A simple, AI-assisted udhaar ledger for small vendors")
st.info("Prototype: always review the AI suggestion before saving. Balances are calculated by Python/SQLite, not by AI.")

with st.sidebar:
    st.subheader("AI setup")
    st.write("Gemma runs locally through an Ollama-compatible endpoint.")
    st.code("ollama pull gemma4:e4b\nollama serve", language="bash")
    st.caption("If your Ollama version does not provide this exact model tag, check available Gemma 4 tags and set GEMMA_MODEL accordingly.")

entry, ledger, history = st.tabs(["Add transaction", "Customer balances", "History & summary"])
with entry:
    st.subheader("What happened?")
    st.write('Example: “Ramesh paid ₹500” or “Suresh ko ₹200 ka chawal udhaar diya.”')
    audio = st.audio_input("Record a short transaction (audio transcription setup is next)")
    if audio is not None:
        st.warning("Audio received. The current starter build does not transcribe it yet; use the text box below for this first end-to-end test.")
    spoken_text = st.text_area("Transaction text", placeholder="Type what the vendor said…", height=100)
    if st.button("Ask Gemma to understand", type="primary"):
        try:
            st.session_state["draft"] = extract_transaction(spoken_text)
        except Exception as exc:
            st.error(f"Could not contact Gemma or parse the transaction: {exc}")
            st.caption("Check that your local model server is running and GEMMA_MODEL matches an installed model.")

    draft = st.session_state.get("draft")
    if draft:
        st.divider()
        st.subheader("Review before saving")
        if draft["needs_clarification"]:
            st.warning(draft["clarification_reason"] or "Please check the amount and transaction type before saving.")
        types = ["credit_sale", "payment_received", "cash_expense", "unknown"]
        selected_type = st.selectbox("Transaction type", types, index=types.index(draft["transaction_type"]))
        customer = st.text_input("Customer name (required for sale/payment)", value=draft["customer_name"])
        amount_value = draft["amount"] if draft["amount"] is not None else 1.0
        amount = st.number_input("Amount (₹)", min_value=0.01, value=float(amount_value), step=10.0)
        description = st.text_input("Item / note", value=draft["description"])
        confirmed = st.checkbox("I checked the details and confirm this transaction")
        if st.button("Save confirmed transaction"):
            if not confirmed:
                st.error("Tick the confirmation box before saving.")
            elif selected_type == "unknown":
                st.error("Choose a clear transaction type before saving.")
            else:
                try:
                    txn_id = add_transaction(customer_name=customer or None, transaction_type=selected_type,
                                             amount=amount, description=description, db_path=DB_PATH)
                    st.success(f"Saved transaction #{txn_id}.")
                    st.session_state.pop("draft", None)
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

with ledger:
    st.subheader("Outstanding customer balances")
    balances = customer_balances(DB_PATH)
    if balances:
        st.dataframe(balances, use_container_width=True, hide_index=True)
    else:
        st.write("No customers yet. Add and confirm your first transaction.")

with history:
    st.subheader("Today's summary")
    summary = daily_summary(DB_PATH)
    c1, c2, c3 = st.columns(3)
    c1.metric("Credit sales", f"₹{summary['credit_sales']:,.2f}")
    c2.metric("Payments received", f"₹{summary['payments']:,.2f}")
    c3.metric("Cash expenses", f"₹{summary['expenses']:,.2f}")
    st.subheader("Recent transactions")
    rows = transaction_history(db_path=DB_PATH)
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.write("No transactions recorded yet.")
