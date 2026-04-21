import streamlit as st
import requests

st.set_page_config(page_title=""Finance Tracker Pro"", layout=""wide"")

if 'token' not in st.session_state:
    st.session_state.token = None

st.title(""🚀 Finance Tracker Pro"")

if not st.session_state.token:
    with st.form(""login_form""):
        username = st.text_input(""Username"")
        password = st.text_input(""Password"", type=""password"")
        if st.form_submit_button(""Login""):
            try:
                response = requests.post(""http://localhost:8000/auth/token"",
                                         data={""username"": username, ""password"": password})
                if response.status_code == 200:
                    st.session_state.token = response.json()[""access_token""]
                    st.success(""Logged in!"")
                    st.experimental_rerun()
                else:
                    st.error(""Invalid credentials"")
            except:
                st.error(""Backend server not running"")
else:
    st.success(""Logged in"")
    headers = {""Authorization"": f""Bearer {st.session_state.token}""}
    st.write(""Welcome to your Finance Dashboard!"")
    if st.button(""Logout""):
        st.session_state.token = None
        st.experimental_rerun()
