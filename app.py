import streamlit as st
import pandas as pd

st.title("Accounts Receivable Aging Summary Generator")

uploaded_file = st.file_uploader("Upload Aging Report", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Aging columns expected in report
    aging_cols = [
        "Current",
        "30 Days",
        "60 Days",
        "90 Days",
        "120 Days",
        "150 Days",
        "180+ Days"
    ]

    # check if columns exist
    missing = [c for c in aging_cols if c not in df.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
    else:

        totals = df[aging_cols].sum()
        total_balance = totals.sum()

        percentages = (totals / total_balance) * 100

        st.subheader("Accounts Receivable Aging Summary")

        st.write("### Total Accounts Receivable Balance")
        st.write(f"${total_balance:,.2f}")

        st.write("### Aging Breakdown")

        summary_table = pd.DataFrame({
            "Aging Category": aging_cols,
            "Amount": totals.values,
            "% of Total": percentages.values
        })

        st.dataframe(summary_table)

        st.write("### Key Observations")

        current_pct = percentages["Current"]
        thirty_pct = percentages["30 Days"]

        st.write(
            f"• {current_pct:.1f}% of receivables fall within the current period, indicating relatively healthy collections."
        )

        st.write(
            f"• {thirty_pct:.1f}% of receivables are within 30 days, suggesting most balances are still collectible."
        )

        over_60 = totals["60 Days"] + totals["90 Days"]
        over_60_pct = (over_60 / total_balance) * 100

        st.write(
            f"• Accounts between 60 and 90 days represent {over_60_pct:.1f}% of receivables and should be monitored."
        )

        over_120 = totals["120 Days"] + totals["150 Days"] + totals["180+ Days"]
        over_120_pct = (over_120 / total_balance) * 100

        st.write(
            f"• Accounts older than 120 days represent {over_120_pct:.1f}% of receivables and may pose collection risk."
        )

        st.success("Summary Generated Successfully")
