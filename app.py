import streamlit as st
import pandas as pd

st.title("Accounts Receivable Aging Summary Generator")

uploaded_file = st.file_uploader("Upload Aging Excel File", type=["xlsx"])


# FUNCTION: Detect header row automatically
def detect_header(file):
    preview = pd.read_excel(file, header=None)

    for i in range(10):
        row = preview.iloc[i].astype(str).str.lower()

        if any("provider" in x for x in row) or any("balance" in x for x in row):
            return i

    return 0


if uploaded_file:

    # Detect correct header row
    header_row = detect_header(uploaded_file)

    st.write(f"Detected header row: {header_row}")

    # Read file using detected header
    df = pd.read_excel(uploaded_file, header=header_row)

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    st.write("Detected Columns:", list(df.columns))

    # Detect aging columns
    aging_map = {
        "Current": ["current", "0-30", "0_30"],
        "30 Days": ["30", "31-60"],
        "60 Days": ["60", "61-90"],
        "90 Days": ["90", "91-120"],
        "120 Days": ["120"],
        "150 Days": ["150"],
        "180+ Days": ["180"]
    }

    detected = {}

    for col in df.columns:
        col_lower = str(col).lower()

        for bucket, keywords in aging_map.items():
            if any(word in col_lower for word in keywords):
                detected[bucket] = col

    st.write("Detected Aging Buckets:", detected)

    if len(detected) == 0:
        st.error("Could not detect aging columns.")
    else:

        totals = {}

        for bucket, column in detected.items():
            totals[bucket] = df[column].sum()

        total_balance = sum(totals.values())

        percentages = {}

        for k, v in totals.items():
            percentages[k] = (v / total_balance) * 100 if total_balance != 0 else 0

        st.subheader("Accounts Receivable Aging Summary")

        st.write("### Total Accounts Receivable Balance")
        st.write(f"${total_balance:,.2f}")

        # Create aging breakdown table
        aging_table = pd.DataFrame({
            "Aging Category": totals.keys(),
            "Amount": totals.values(),
            "% of Total": [f"{p:.1f}%" for p in percentages.values()]
        })

        st.write("### Aging Breakdown")
        st.dataframe(aging_table)

        # Observations
        st.write("### Key Observations")

        if "Current" in percentages:
            st.write(
                f"• {percentages['Current']:.1f}% of receivables fall within the current period, indicating relatively healthy collections."
            )

        if "30 Days" in percentages:
            st.write(
                f"• {percentages['30 Days']:.1f}% of receivables fall within the 30-day category."
            )

        if "60 Days" in totals and "90 Days" in totals:
            mid_term = totals["60 Days"] + totals["90 Days"]
            mid_pct = (mid_term / total_balance) * 100
            st.write(
                f"• Accounts between 60–90 days total ${mid_term:,.2f} ({mid_pct:.1f}% of receivables)."
            )

        long_term = (
            totals.get("120 Days", 0)
            + totals.get("150 Days", 0)
            + totals.get("180+ Days", 0)
        )

        if long_term > 0:
            long_pct = (long_term / total_balance) * 100
            st.write(
                f"• Accounts older than 120 days total ${long_term:,.2f} ({long_pct:.1f}% of receivables)."
            )

        st.success("Summary Generated Successfully")
