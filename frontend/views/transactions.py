import streamlit as st
import requests
import pandas as pd
from utils.app_config import apply_theme, money

API_URL = "http://127.0.0.1:8000"


def main():
    apply_theme()

    st.markdown("""
    <style>
        .page-title {
            font-size: 34px;
            font-weight: 800;
            color: #173b2c;
            margin-bottom: 5px;
        }

        .page-subtitle {
            color: #6b7c72;
            font-size: 16px;
            margin-bottom: 25px;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 800;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">Transactions</div>
    <div class="page-subtitle">View, add, edit and delete your transactions.</div>
    """, unsafe_allow_html=True)

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    try:
        response = requests.get(f"{API_URL}/transactions/", headers=headers)
        transactions = response.json() if response.status_code == 200 else []
    except Exception:
        transactions = []

    with st.expander("➕ Add New Transaction", expanded=False):
        amount = st.number_input("Amount", min_value=0.01, step=1.0, key="add_amount")
        category = st.text_input("Category", placeholder="Food, Salary, Shopping", key="add_category")
        description = st.text_input("Description", placeholder="Short description", key="add_description")
        tx_type = st.selectbox("Type", ["INCOME", "EXPENSE"], key="add_type")

        if st.button("Add Transaction"):
            data = {
                "amount": amount,
                "category": category,
                "description": description,
                "transaction_type": tx_type,
            }

            r = requests.post(f"{API_URL}/transactions/", json=data, headers=headers)

            if r.status_code in [200, 201]:
                st.success("Transaction added successfully!")
                st.rerun()
            else:
                st.error(f"Failed to add transaction. Status: {r.status_code}")
                st.write(r.text)

    st.markdown("### Transaction List")

    if not transactions:
        st.info("No transactions available.")
        return

    df = pd.DataFrame(transactions)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    if "amount" in df.columns:
        df["amount"] = df["amount"].apply(money)

    show_cols = ["description", "category", "date", "amount", "transaction_type"]
    show_cols = [col for col in show_cols if col in df.columns]

    st.dataframe(df[show_cols], use_container_width=True, hide_index=True)

    st.markdown("### Edit or Delete Transaction")

    transaction_options = {}

    for tx in transactions:
        raw_date = tx.get("date", "")

        try:
            clean_date = pd.to_datetime(raw_date).strftime("%Y-%m-%d")
        except Exception:
            clean_date = raw_date

        label = (
            f"{tx.get('description', 'No description')}  |  "
            f"{tx.get('category', 'No category')}  |  "
            f"{money(tx.get('amount', 0))}  |  "
            f"{clean_date}"
        )

        transaction_options[label] = tx

    selected_label = st.selectbox(
        "Choose transaction",
        list(transaction_options.keys())
    )

    selected_tx = transaction_options[selected_label]
    transaction_id = selected_tx["id"]

    with st.form("edit_transaction_form"):
        edit_amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=1.0,
            value=float(selected_tx.get("amount", 0.01)),
            key="edit_amount"
        )

        edit_category = st.text_input(
            "Category",
            value=selected_tx.get("category", ""),
            key="edit_category"
        )

        edit_description = st.text_input(
            "Description",
            value=selected_tx.get("description", ""),
            key="edit_description"
        )

        current_type = selected_tx.get("transaction_type", "EXPENSE").upper()

        edit_type = st.selectbox(
            "Type",
            ["INCOME", "EXPENSE"],
            index=0 if current_type == "INCOME" else 1,
            key="edit_type"
        )

        update_btn = st.form_submit_button("Save Changes")

        if update_btn:
            update_data = {
                "amount": edit_amount,
                "category": edit_category,
                "description": edit_description,
                "transaction_type": edit_type,
            }

            r = requests.put(
                f"{API_URL}/transactions/{transaction_id}",
                json=update_data,
                headers=headers
            )

            if r.status_code in [200, 204]:
                st.success("Transaction updated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to update transaction. Status: {r.status_code}")
                st.write(r.text)

    delete_confirm = st.checkbox("I confirm that I want to delete this transaction")

    if st.button("🗑️ Delete Selected Transaction"):
        if not delete_confirm:
            st.warning("Please confirm before deleting.")
        else:
            r = requests.delete(
                f"{API_URL}/transactions/{transaction_id}",
                headers=headers
            )

            if r.status_code in [200, 204]:
                st.success("Transaction deleted successfully!")
                st.rerun()
            else:
                st.error(f"Failed to delete transaction. Status: {r.status_code}")
                st.write(r.text)