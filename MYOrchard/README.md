# MYOrchard — Mango Wholesale Analytics Portfolio

**A complete synthetic portfolio project** using Python, SQL and Power BI to explore 15 mango harvest seasons (2011–12 to 2025–26).

> All businesses, people, transactions, quantities, prices, costs and results are fictional. This is not real orchard data or a claim about actual local conditions.

## Run it on Windows
Install Python 3.11+ from https://www.python.org/downloads/ (select **Add Python to PATH** during setup). Open this folder in File Explorer, click the address bar, type `cmd`, press Enter, then run:

```bat
py -m pip install -r requirements.txt
py src\run_project.py
py -m unittest discover -s tests -v
```

The ZIP already includes generated CSV data and analysis outputs. Running the script regenerates them reproducibly.

## What's included
- `data/raw/`: seasons, fictional buyers, varieties, orchard blocks, harvest, sales, expenses
- `data/processed/`: seasonal KPIs, buyer and variety performance, monthly sales, quality report
- `src/`: generator, analysis and validation code
- `sql/`: schema and business questions
- `dashboard/`: Power BI dashboard guide
- `reports/`: portfolio case study
- `docs/`: data dictionary, assumptions and GitHub upload guide
- `tests/`: automated integrity tests

## Metrics
Revenue = quantity × price less discount. Operating contribution = revenue less the expense categories included in this simplified model; it is not audited net profit and excludes tax, financing, depreciation and unmodelled costs. Wastage rate = rejected kg / harvested kg. Collection rate = collected amount / invoiced revenue.

The pandemic, weather and market-pressure flags are **synthetic scenario assumptions**, not measured historical impacts. Always label the dataset as synthetic in your portfolio. 
