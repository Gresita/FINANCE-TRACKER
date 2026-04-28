import streamlit as st
from views import login_register, dashboard, transactions, analytics, settings
from components import sidebar
from views import login_register, dashboard, transactions, analytics, settings, admin_dashboard
st.set_page_config(page_title="Finance Tracker", page_icon="💸", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    login_register.main()
else:
    page = sidebar.show_sidebar()

    if page == "Dashboard":
        dashboard.main()
    elif page == "Transactions":
        transactions.main()
    elif page == "Analytics":
        analytics.main()
    elif page == "Settings":
        settings.main()
    elif page == "Admin":
        admin_dashboard.main()
if "role" not in st.session_state:
    st.session_state.role = None