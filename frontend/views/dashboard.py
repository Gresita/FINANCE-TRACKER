import streamlit as st
import requests
import pandas as pd
from components.metric_card import metric_card
from utils.app_config import apply_theme, money

API_URL = "http://127.0.0.1:8000"


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

        .metric-card {
            background: white;
            padding: 24px;
            border-radius: 22px;
            box-shadow: 0 12px 30px rgba(22, 60, 44, 0.08);
            border: 1px solid #dceee5;
            min-height: 135px;
        }

        .metric-top {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
        }

        .metric-icon {
            font-size: 26px;
            background: #e8f7ef;
            padding: 8px;
            border-radius: 14px;
        }

        .metric-title {
            color: #6b7c72;
            font-size: 15px;
            font-weight: 700;
        }

        .metric-value {
            font-size: 30px;
            font-weight: 800;
            color: #173b2c;
        }

        .dashboard-card {
            background: white;
            padding: 25px;
            border-radius: 22px;
            border: 1px solid #dceee5;
            box-shadow: 0 12px 30px rgba(22, 60, 44, 0.06);
            margin-top: 25px;
        }

        .card-title {
            color: #173b2c;
            font-size: 22px;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .card-text {
            color: #6b7c72;
            font-size: 15px;
            margin-bottom: 0;
        }

        .health-good {
            color: #2e9f68;
            font-weight: 900;
            font-size: 24px;
        }

        .health-warning {
            color: #d97706;
            font-weight: 900;
            font-size: 24px;
        }

        .health-danger {
            color: #dc2626;
            font-weight: 900;
            font-size: 24px;
        }

        .stButton > button {
            width: 100%;
            height: 45px;
            border-radius: 12px;
            background: #2e9f68;
            color: white;
            font-weight: 800;
            border: none;
        }

        .stButton > button:hover {
            background: #278b5b;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">Dashboard</div>
    <div class="page-subtitle">
        Your financial overview, salary updates, recent activity and saving insights.
    </div>
    """, unsafe_allow_html=True)

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    try:
        summary = requests.get(f"{API_URL}/transactions/summary", headers=headers).json()
    except Exception:
        st.error("Failed to fetch summary")
        summary = {"balance": 0, "total_income": 0, "total_expense": 0}

    try:
        response = requests.get(f"{API_URL}/transactions/", headers=headers)
        transactions = response.json() if response.status_code == 200 else []
    except Exception:
        transactions = []

    balance = float(summary.get("balance", 0))
    total_income = float(summary.get("total_income", 0))
    total_expense = float(summary.get("total_expense", 0))

    col1, col2, col3 = st.columns(3)

    metric_card(col1, "Balance", money(balance), "💼")
    metric_card(col2, "Total Income", money(total_income), "📈")
    metric_card(col3, "Total Expense", money(total_expense), "📉")

    spent_percent = 0
    savings_rate = 0

    if total_income > 0:
        spent_percent = min((total_expense / total_income) * 100, 100)
        savings_rate = max(((total_income - total_expense) / total_income) * 100, 0)

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Financial Health</div>', unsafe_allow_html=True)

    if total_income == 0:
        st.markdown('<div class="health-warning">Add your first income to start tracking.</div>', unsafe_allow_html=True)
        st.progress(0)
        st.markdown('<p class="card-text">Your dashboard becomes more useful once you add salary or income.</p>', unsafe_allow_html=True)
    elif total_expense <= total_income * 0.5:
        st.markdown('<div class="health-good">Great! You are saving well.</div>', unsafe_allow_html=True)
        st.progress(int(spent_percent))
        st.markdown(f'<p class="card-text">You spent {spent_percent:.1f}% of your income. Savings rate: {savings_rate:.1f}%.</p>', unsafe_allow_html=True)
    elif total_expense <= total_income:
        st.markdown('<div class="health-warning">Careful, your expenses are getting high.</div>', unsafe_allow_html=True)
        st.progress(int(spent_percent))
        st.markdown(f'<p class="card-text">You spent {spent_percent:.1f}% of your income. Savings rate: {savings_rate:.1f}%.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="health-danger">You are spending more than your income.</div>', unsafe_allow_html=True)
        st.progress(100)
        st.markdown('<p class="card-text">Try reducing expenses or adding more income.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Quick Add Salary</div>', unsafe_allow_html=True)
        st.markdown('<p class="card-text">Add salary or any income directly from Dashboard.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        with st.form("quick_salary_form"):
            salary_amount = st.number_input("Salary amount", min_value=0.01, step=10.0)
            salary_description = st.text_input("Description", value="Monthly salary")
            salary_category = st.text_input("Category", value="Salary")

            submitted = st.form_submit_button("Add Salary")

            if submitted:
                data = {
                    "amount": salary_amount,
                    "description": salary_description,
                    "category": salary_category,
                    "transaction_type": "INCOME"
                }

                r = requests.post(f"{API_URL}/transactions/", json=data, headers=headers)

                if r.status_code in [200, 201]:
                    st.success("Salary added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add salary")

    with col5:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Top Spending Category</div>', unsafe_allow_html=True)

        if transactions:
            df = pd.DataFrame(transactions)

            if not df.empty and "transaction_type" in df.columns:
                df["transaction_type"] = df["transaction_type"].str.lower()
                expense_df = df[df["transaction_type"] == "expense"]

                if not expense_df.empty:
                    top_category = (
                        expense_df.groupby("category")["amount"]
                        .sum()
                        .sort_values(ascending=False)
                        .reset_index()
                        .iloc[0]
                    )

                    st.markdown(
                        f"""
                        <div class="health-warning">{top_category['category']}</div>
                        <p class="card-text">You spent {money(top_category['amount'])} in this category.</p>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<p class="card-text">No expenses yet.</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="card-text">No valid transaction data.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="card-text">No transactions yet.</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Recent Transactions</div>', unsafe_allow_html=True)

    if transactions:
        df = pd.DataFrame(transactions)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        if "amount" in df.columns:
            df["amount"] = df["amount"].apply(money)

        show_cols = ["description", "category", "date", "amount", "transaction_type"]
        show_cols = [col for col in show_cols if col in df.columns]

        st.dataframe(df[show_cols].tail(5), use_container_width=True, hide_index=True)
    else:
        st.markdown('<p class="card-text">No transactions available yet.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)