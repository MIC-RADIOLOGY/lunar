import streamlit as st
import pandas as pd

st.title("Accounts Receivable Aging Summary Generator")

uploaded_file = st.file_uploader("Upload Aging Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Show columns for debugging
    st.write("Detected Columns:", list(df.columns))

    # Detect aging columns automatically
    aging_map = {
        "current": ["current", "0-30", "0_30"],
        "30": ["30", "31-60", "30 days"],
        "60": ["60", "61-90", "60 days"],
        "90": ["90", "91-120", "90 days"],
        "120": ["120", "121-150"],
        "150": ["150", "151-180"],
        "180+": ["180", "180+", "180 plus"]
    }

    detected = {}

    for col in df.columns:
        col_lower = str(col).lower()

        for key, values in aging_map.items():
            if any(v in col_lower for v in values):
                detected[key] = col

    st.write("Detected Aging Buckets:", detected)

    if len(detected) < 3:
        st.error("Could not detect aging columns correctly.")
    else:

        totals = {}

        for bucket, col in detected.items():
            totals[bucket] = df[col].sum()

        total_balance = sum(totals.values())

        percentages = {
            k: (v / total_balance) * 100 if total_balance != 0 else 0
            for k, v in totals.items()
        }

        st.subheader("Accounts Receivable Aging Summary")

        st.write("### Total Accounts Receivable Balance")
        st.write(f"${total_balance:,.2f}")

        # Aging Table
        aging_table = pd.DataFrame({
            "Aging Category": totals.keys(),
            "Amount": totals.values(),
            "% of Total": [f"{p:.1f}%" for p in percentages.values()]
        })

        st.write("### Aging Breakdown")
        st.dataframe(aging_table)

        # Observations
        st.write("### Key Observations")

        if "current" in percentages:
            st.write(
                f"• {percentages['current']:.1f}% of receivables fall within the current period, indicating relatively healthy collections."
            )

        if "30" in percentages:
            st.write(
                f"• {percentages['30']:.1f}% of receivables fall within the 30-day category."
            )

        if "60" in totals and "90" in totals:
            mid = totals["60"] + totals["90"]
            mid_pct = (mid / total_balance) * 100
            st.write(
                f"• Accounts between 60 and 90 days total ${mid:,.2f} ({mid_pct:.1f}% of receivables)."
            )

        if "120" in totals or "150" in totals or "180+" in totals:
            long_term = totals.get("120",0) + totals.get("150",0) + totals.get("180+",0)
            long_pct = (long_term / total_balance) * 100
            st.write(
                f"• Accounts older than 120 days total ${long_term:,.2f} ({long_pct:.1f}% of receivables)."
            )

        st.success("Summary Generated Successfully")
