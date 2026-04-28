import streamlit as st
import requests
import pandas as pd
from utils.app_config import apply_theme, money

API_URL = "http://127.0.0.1:8000"


def main():
    apply_theme()

    if st.session_state.get("role") != "admin":
        st.error("Access denied. Admin only.")
        return

    st.title("Admin Dashboard")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    try:
        summary = requests.get(f"{API_URL}/admin/summary", headers=headers).json()
        users = requests.get(f"{API_URL}/admin/users", headers=headers).json()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    # 🔥 SUMMARY
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Users", summary.get("total_users", 0))
    col2.metric("Transactions", summary.get("total_transactions", 0))
    col3.metric("Income", money(summary.get("total_income", 0)))
    col4.metric("Expense", money(summary.get("total_expense", 0)))

    st.divider()

    # 👥 USERS TABLE
    st.subheader("Users")

    df = pd.DataFrame(users)

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # 🔧 MANAGE USERS
    st.subheader("Manage Users")

    user_options = {
        f"{u['username']} | {u['email']} | {u['role']}": u
        for u in users
    }

    selected_label = st.selectbox("Select user", list(user_options.keys()))
    selected_user = user_options[selected_label]
    user_id = selected_user["id"]

    new_role = st.selectbox(
        "Change role",
        ["user", "admin"],
        index=0 if selected_user["role"] == "user" else 1
    )

    col_a, col_b = st.columns(2)

    # 🔁 UPDATE ROLE
    with col_a:
        if st.button("Update Role"):
            r = requests.put(
                f"{API_URL}/admin/users/{user_id}/role",
                json={"role": new_role},
                headers=headers
            )

            if r.status_code == 200:
                st.success("Role updated!")
                st.rerun()
            else:
                st.error(f"Error: {r.status_code}")
                st.write(r.text)

    # ❌ DELETE USER
    with col_b:
        confirm = st.checkbox("Confirm delete")

        if st.button("Delete User"):
            if not confirm:
                st.warning("Confirm deletion first")
            else:
                r = requests.delete(
                    f"{API_URL}/admin/users/{user_id}",
                    headers=headers
                )

                if r.status_code == 200:
                    st.success("User deleted!")
                    st.rerun()
                else:
                    st.error(f"Error: {r.status_code}")
                    st.write(r.text)