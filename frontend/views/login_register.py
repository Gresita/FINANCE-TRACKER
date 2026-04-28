import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def api_login(username, password):
    try:
        r = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password}
        )

        if r.status_code == 200:
            return True, r.json()

        try:
            return False, r.json().get("detail", "Invalid username or password")
        except Exception:
            return False, "Invalid username or password"

    except Exception:
        return False, "Could not connect to the server"


def api_register(username, email, password):
    try:
        r = requests.post(
            f"{API_URL}/auth/register",
            json={"username": username, "email": email, "password": password}
        )

        if r.status_code == 201:
            return True, "Registration successful! Please login."

        try:
            detail = r.json().get("detail", "Registration failed")

            if isinstance(detail, list):
                message = detail[0].get("msg", "Registration failed")
            else:
                message = detail

            return False, message

        except Exception:
            return False, "Registration failed"

    except Exception:
        return False, "Could not connect to the server"


def main():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f3fff8 0%, #e8f7ef 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .auth-wrapper {
            max-width: 430px;
            margin: 40px auto 0 auto;
        }

        .logo-box {
            width: 70px;
            height: 70px;
            background: #2e9f68;
            color: white;
            border-radius: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            margin: 0 auto 18px auto;
            box-shadow: 0 12px 30px rgba(46, 159, 104, 0.25);
        }

        .main-title {
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            color: #173b2c;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #6b7c72;
            font-size: 16px;
            margin-bottom: 28px;
        }

        .auth-card {
            background: white;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 18px 45px rgba(22, 60, 44, 0.12);
            border: 1px solid #dceee5;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f0f7f3;
            padding: 6px;
            border-radius: 14px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 11px;
            font-weight: 700;
            color: #476257;
        }

        .stTabs [aria-selected="true"] {
            background-color: white;
            color: #2e9f68;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        label {
            font-weight: 700 !important;
            color: #264b3b !important;
        }

        .stTextInput input {
            height: 48px;
            border-radius: 12px;
            border: 1px solid #d5e8df;
            background-color: #fbfffd;
            font-size: 15px;
        }

        .stTextInput input:focus {
            border-color: #2e9f68;
            box-shadow: 0 0 0 2px rgba(46, 159, 104, 0.15);
        }

        .stButton > button {
            width: 100%;
            height: 48px;
            border-radius: 13px;
            background: #2e9f68;
            color: white;
            font-weight: 800;
            font-size: 16px;
            border: none;
            margin-top: 10px;
            box-shadow: 0 10px 22px rgba(46, 159, 104, 0.25);
        }

        .stButton > button:hover {
            background: #278b5b;
            color: white;
        }

        .footer-text {
            text-align: center;
            color: #7c8f85;
            font-size: 14px;
            margin-top: 22px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="auth-wrapper">
        <div class="logo-box">💸</div>
        <div class="main-title">Finance Tracker</div>
        <div class="subtitle">Manage your finances with ease</div>
        
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input(
            "👤 Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button("Sign In"):
            if username and password:
                success, result = api_login(username, password)

                if success:
                    st.session_state.token = result.get("access_token")
                    st.session_state.role = result.get("role")
                    st.session_state.username = result.get("username")
                    st.session_state.email = result.get("email")

                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("Please fill all fields")

    with tab2:
        username = st.text_input(
            "👤 Username",
            placeholder="Choose a username",
            key="register_username"
        )

        email = st.text_input(
            "✉️ Email",
            placeholder="Enter your email",
            key="register_email"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        if st.button("Create Account"):
            if username and email and password:
                success, message = api_register(username, email, password)

                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please fill all fields")

    st.markdown("""
        </div>
        <div class="footer-text">
            Secure login with encrypted data transmission
        </div>
    </div>
    """, unsafe_allow_html=True)