import streamlit as st


def metric_card(st_module, title, value, icon="💰"):
    st_module.markdown(f"""
    <div class="metric-card">
        <div class="metric-top">
            <span class="metric-icon">{icon}</span>
            <span class="metric-title">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)