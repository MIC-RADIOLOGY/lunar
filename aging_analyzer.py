import pandas as pd

def analyze_aging(df):

    # aging columns
    aging_cols = [
        "Current",
        "30 Days",
        "60 Days",
        "90 Days",
        "120 Days",
        "150 Days",
        "180+ Days"
    ]

    # totals
    totals = df[aging_cols].sum()
    total_balance = totals.sum()

    # percentages
    percentages = (totals / total_balance) * 100

    summary = {
        "total_balance": total_balance,
        "totals": totals,
        "percentages": percentages
    }

    return summary


def generate_report(summary):

    t = summary["totals"]
    p = summary["percentages"]
    total = summary["total_balance"]

    report = f"""
Accounts Receivable Aging Summary

Total Accounts Receivable Balance:
${total:,.2f}

Aging Breakdown

Current: ${t['Current']:,.2f} ({p['Current']:.1f}%)
30 Days: ${t['30 Days']:,.2f} ({p['30 Days']:.1f}%)
60 Days: ${t['60 Days']:,.2f} ({p['60 Days']:.1f}%)
90 Days: ${t['90 Days']:,.2f} ({p['90 Days']:.1f}%)
120 Days: ${t['120 Days']:,.2f} ({p['120 Days']:.1f}%)
150 Days: ${t['150 Days']:,.2f} ({p['150 Days']:.1f}%)
180+ Days: ${t['180+ Days']:,.2f} ({p['180+ Days']:.1f}%)
"""

    return report
