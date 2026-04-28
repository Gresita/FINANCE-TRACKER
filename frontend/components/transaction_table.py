import streamlit as st
import pandas as pd


def transaction_table(transactions):
    if not transactions:
        st.markdown("""
        <div class="empty-box">
            <h3>No transactions yet</h3>
            <p>Add your first transaction to start tracking your finances.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(transactions)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    columns = ["description", "category", "date", "amount", "transaction_type"]
    df = df[[col for col in columns if col in df.columns]]

    st.dataframe(df, use_container_width=True, hide_index=True)