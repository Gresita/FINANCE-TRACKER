import streamlit as st

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "CHF": "CHF "
}


def init_preferences():
    if "currency" not in st.session_state:
        st.session_state.currency = "USD"

    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Light"

    if "savings_goal" not in st.session_state:
        st.session_state.savings_goal = 1000.0


def money(value):
    init_preferences()
    symbol = CURRENCY_SYMBOLS.get(st.session_state.currency, "$")
    return f"{symbol}{float(value):,.2f}"


def apply_theme():
    init_preferences()

    if st.session_state.theme_mode == "Dark":
        st.markdown("""
        <style>
            .stApp {
                background: #0f1f18 !important;
                color: #f2fff8 !important;
            }

            .page-title,
            .card-title,
            .metric-value,
            .crypto-price {
                color: #f2fff8 !important;
            }

            .page-subtitle,
            .card-text,
            .metric-title,
            .crypto-label {
                color: #b7cfc3 !important;
            }

            .metric-card,
            .dashboard-card,
            .settings-card,
            .analytics-card {
                background: #173b2c !important;
                border: 1px solid #2e6b4f !important;
                box-shadow: none !important;
            }

            [data-testid="stDataFrame"] {
                background: #173b2c !important;
            }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
            .stApp {
                background: #f5fbf8 !important;
            }
        </style>
        """, unsafe_allow_html=True)