# Accounts Receivable Aging Summary App

This is a Streamlit application that automatically generates an **Accounts Receivable Aging Summary Report** from an uploaded Excel aging report.

The app calculates:
- Total accounts receivable balance
- Aging category totals
- Percentage of receivables per aging bucket
- Key observations for management reporting

## Features

- Upload Excel aging report
- Automatic aging analysis
- Generates management-ready summary
- Simple and fast interface

## Requirements

Python 3.9+

Required packages:

- streamlit
- pandas
- openpyxl

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Run the application using:

```bash
streamlit run app.py
```

The app will open in your browser where you can upload the aging Excel file.

## Expected Aging Columns

The Excel file should contain the following aging categories:

- Current
- 30 Days
- 60 Days
- 90 Days
- 120 Days
- 150 Days
- 180+ Days

## Project Structure

```
aging-summary-app
│
├── app.py
├── requirements.txt
└── README.md
```

## Purpose

This tool helps finance teams quickly analyze debtor aging and produce **management summaries for reporting and decision making**.
