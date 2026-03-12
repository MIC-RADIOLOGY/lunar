import streamlit as st
import pandas as pd
from aging_analyzer import analyze_aging, generate_report

st.title("Accounts Receivable Aging Analyzer")

uploaded_file = st.file_uploader("Upload Aging Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.write("Preview of Data")
    st.dataframe(df.head())

    summary = analyze_aging(df)

    report = generate_report(summary)

    st.subheader("Generated Management Summary")

    st.text(report)
