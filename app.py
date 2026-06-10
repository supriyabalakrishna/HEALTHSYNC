import streamlit as st

from agents.emergency_agent import (
    analyze_emergency
)

st.set_page_config(
    page_title="Urban Guardian AI"
)

st.title(
    "🚑 Urban Guardian AI"
)

emergency = st.text_area(
    "Enter Emergency"
)

if st.button(
    "Analyze Emergency"
):

    result = analyze_emergency(
        emergency
    )

    st.subheader(
        "AI Analysis"
    )

    st.code(
        result,
        language="json"
    )