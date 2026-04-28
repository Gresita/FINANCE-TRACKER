import streamlit as st
from utils.app_config import apply_theme, init_preferences, money


def main():
    init_preferences()
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

        .settings-card {
            background: white;
            padding: 28px;
            border-radius: 24px;
            border: 1px solid #dceee5;
            box-shadow: 0 12px 30px rgba(22, 60, 44, 0.07);
            margin-bottom: 25px;
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
        }

        .profile-avatar {
            width: 72px;
            height: 72px;
            background: #2e9f68;
            color: white;
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            box-shadow: 0 10px 24px rgba(46, 159, 104, 0.25);
            margin-bottom: 12px;
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
    <div class="page-title">Settings</div>
    <div class="page-subtitle">Personalize your Finance Tracker experience.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="settings-card">
            <div class="profile-avatar">👤</div>
            <div class="card-title">Profile</div>
            <p class="card-text">
                Logged in successfully with secure JWT authentication.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="settings-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">App Preferences</div>', unsafe_allow_html=True)

        currency = st.selectbox(
            "Preferred Currency",
            ["USD", "EUR", "GBP", "CHF"],
            index=["USD", "EUR", "GBP", "CHF"].index(st.session_state.currency)
        )

        theme_mode = st.selectbox(
            "Theme Mode",
            ["Light", "Dark"],
            index=["Light", "Dark"].index(st.session_state.theme_mode)
        )

        savings_goal = st.number_input(
            "Monthly Savings Goal",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.savings_goal)
        )

        if st.button("Save Preferences"):
            st.session_state.currency = currency
            st.session_state.theme_mode = theme_mode
            st.session_state.savings_goal = savings_goal
            st.success("Preferences saved successfully!")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Current Preferences</div>', unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)

    col3.metric("Currency", st.session_state.currency)
    col4.metric("Theme", st.session_state.theme_mode)
    col5.metric("Savings Goal", money(st.session_state.savings_goal))

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Security</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="card-text">
        Your session is protected with JWT token authentication.
        Use logout from the sidebar when you finish.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)