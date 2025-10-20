# Call Records Dashboard

Interactive dashboard for analyzing call records from PDF files. Users can upload single or multiple PDFs and explore multiple graphs for call analytics.

## Features

* Upload **single or multiple PDF** call records.
* View **Top N contacts** and **Top Used Usage**.
* **Call distribution**: Billed, Free, and Chargeable usage.
* **Calls over time** and **total call time** visualizations.
* **Search by number** with:

  * Daily call duration
  * Number of calls
  * Summary stats (total calls, total duration, average duration)
* Fully interactive graphs using **Plotly**.
* Supports **custom top N selection** and **date-based aggregation**.

## Project Structure

```
call_records_dashboard/
│
├─ app.py                   # Streamlit app entry point
├─ call_records_extractor.py # PDF parsing & DataFrame conversion
├─ graphs.py                # Plotly chart functions
├─ temp/                    # Temporary folder for uploaded CSVs
└─ README.md
```

## Requirements

* Python 3.9+
* Streamlit
* Plotly
* PyPDF2
* Pandas

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run app.py
```

Upload your PDF files and explore the tabs for analytics.
