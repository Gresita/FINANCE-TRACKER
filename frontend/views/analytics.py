import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils.app_config import apply_theme, money

API_URL = "http://127.0.0.1:8000"
COINGECKO_URL = "https://api.coingecko.com/api/v3"

REQUEST_HEADERS = {
    "accept": "application/json",
    "User-Agent": "FinanceTrackerApp/1.0"
}


def get_transactions(headers):
    try:
        response = requests.get(
            f"{API_URL}/transactions/",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        st.warning(f"Transactions API error: {response.status_code}")

    except Exception as e:
        st.warning(f"Could not load transactions: {e}")

    return []


def get_bitcoin_price():
    try:
        response = requests.get(
            f"{COINGECKO_URL}/simple/price",
            params={
                "ids": "bitcoin",
                "vs_currencies": "usd",
                "include_24hr_change": "true"
            },
            headers=REQUEST_HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            return response.json().get("bitcoin", {})

        st.warning(f"CoinGecko price error: {response.status_code}")

    except Exception as e:
        st.warning(f"Bitcoin price API error: {e}")

    return {}


def get_bitcoin_history(days=30):
    try:
        response = requests.get(
            f"{COINGECKO_URL}/coins/bitcoin/market_chart",
            params={
                "vs_currency": "usd",
                "days": days,
                "interval": "daily"
            },
            headers=REQUEST_HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json().get("prices", [])

            if not data:
                return pd.DataFrame(columns=["date", "price"])

            df = pd.DataFrame(data, columns=["timestamp", "price"])
            df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

            return df[["date", "price"]]

        st.warning(f"CoinGecko history error: {response.status_code}")

    except Exception as e:
        st.warning(f"Bitcoin history API error: {e}")

    return pd.DataFrame(columns=["date", "price"])


def main():
    apply_theme()

    st.markdown("""
    <style>
        .page-title {
            font-size: 36px;
            font-weight: 900;
            color: #173b2c;
            margin-bottom: 5px;
        }

        .page-subtitle {
            color: #6b7c72;
            font-size: 17px;
            margin-bottom: 28px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">Analytics</div>
    <div class="page-subtitle">
        Real-time crypto insights combined with your personal finance analytics.
    </div>
    """, unsafe_allow_html=True)

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    transactions = get_transactions(headers)
    bitcoin_price = get_bitcoin_price()
    bitcoin_history = get_bitcoin_history(days=30)

    price = bitcoin_price.get("usd", 0)
    change = bitcoin_price.get("usd_24h_change", 0)

    # 🔥 FIXED METRICS (replaces broken boxes)
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Bitcoin Current Price",
            value=money(price),
            delta=f"{change:.2f}% (24h)"
        )

    with col2:
        st.metric(
            label="Tracked Coin",
            value="BTC",
            delta="Source: CoinGecko"
        )

    # 📈 BITCOIN GRAPH
    if not bitcoin_history.empty:
        fig = px.line(
            bitcoin_history,
            x="date",
            y="price",
            title="1. Bitcoin Price Trend - Last 30 Days",
            labels={
                "date": "Date",
                "price": f"Price ({st.session_state.currency})"
            }
        )

        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Could not load Bitcoin historical data.")

    # 📊 PERSONAL FINANCE ANALYTICS
    if transactions:
        df = pd.DataFrame(transactions)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.to_period("M").astype(str)

        if "transaction_type" in df.columns:
            df["transaction_type"] = df["transaction_type"].str.lower()

        st.markdown("### Personal Finance Charts")

        col3, col4 = st.columns(2)

        # 🥧 PIE CHART
        with col3:
            expense_df = df[df["transaction_type"] == "expense"]

            if not expense_df.empty:
                category_df = expense_df.groupby("category")["amount"].sum().reset_index()

                fig_pie = px.pie(
                    category_df,
                    names="category",
                    values="amount",
                    title="2. Expenses by Category"
                )

                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expense transactions available.")

        # 📊 BAR CHART
        with col4:
            type_df = df.groupby("transaction_type")["amount"].sum().reset_index()

            fig_bar = px.bar(
                type_df,
                x="transaction_type",
                y="amount",
                title="3. Income vs Expense",
                labels={
                    "transaction_type": "Type",
                    "amount": f"Amount ({st.session_state.currency})"
                }
            )

            st.plotly_chart(fig_bar, use_container_width=True)

        # 📈 MONTHLY TREND
        df["signed_amount"] = df.apply(
            lambda row: row["amount"]
            if row["transaction_type"] == "income"
            else -row["amount"],
            axis=1
        )

        monthly_df = df.groupby("month")["signed_amount"].sum().reset_index()
        monthly_df = monthly_df.rename(columns={"signed_amount": "balance"})

        fig_balance = px.line(
            monthly_df,
            x="month",
            y="balance",
            markers=True,
            title="4. Monthly Balance Trend",
            labels={
                "month": "Month",
                "balance": f"Balance ({st.session_state.currency})"
            }
        )

        fig_balance.update_layout(height=420)
        st.plotly_chart(fig_balance, use_container_width=True)

    else:
        st.info("No transactions available yet.")