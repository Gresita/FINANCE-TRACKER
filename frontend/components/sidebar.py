import streamlit as st


def show_sidebar():
    if "token" not in st.session_state or st.session_state.token is None:
        return None

    st.sidebar.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #173b2c 0%, #245b42 100%);
        }

        .sidebar-title {
            font-size: 28px;
            font-weight: 900;
            color: white;
            margin-bottom: 4px;
        }

        .sidebar-subtitle {
            font-size: 15px;
            color: #d7eee3;
            margin-bottom: 25px;
        }

        .menu-btn {
            margin-bottom: 10px;
        }

        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            height: 48px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.14);
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.25);
            font-size: 17px;
            font-weight: 800;
            text-align: left;
            padding-left: 18px;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: white;
            color: #173b2c !important;
        }

        .active-btn button {
            background: white !important;
            color: #173b2c !important;
        }

        .logout-space {
            margin-top: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    with st.sidebar:
        st.markdown("""
        <div class="sidebar-title">💸 Finance Tracker</div>
        <div class="sidebar-subtitle">Manage your money smarter</div>
        """, unsafe_allow_html=True)

        def menu_button(label, page_name):
            container_class = "active-btn" if st.session_state.page == page_name else ""
            st.markdown(f'<div class="{container_class} menu-btn">', unsafe_allow_html=True)

            if st.button(label):
                st.session_state.page = page_name
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # Normal menu
        menu_button("📊 Dashboard", "Dashboard")
        menu_button("💳 Transactions", "Transactions")
        menu_button("📈 Analytics", "Analytics")
        menu_button("⚙️ Settings", "Settings")

        # 🔥 ADMIN ONLY
        if st.session_state.get("role") == "admin":
            st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
            st.markdown("<div style='color:#d7eee3; font-weight:700;'>ADMIN</div>", unsafe_allow_html=True)

            menu_button("🛡️ Admin Dashboard", "Admin")

        st.markdown('<div class="logout-space"></div>', unsafe_allow_html=True)

        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.role = None
            st.session_state.page = "Dashboard"
            st.rerun()

    return st.session_state.page