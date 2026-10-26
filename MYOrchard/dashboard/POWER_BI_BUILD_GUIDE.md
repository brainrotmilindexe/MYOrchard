# Power BI build guide

Install Power BI Desktop from Microsoft's official page: https://www.microsoft.com/power-platform/products/power-bi/desktop

Use **Get data → Text/CSV** to import `data/processed/seasonal_kpis.csv`, `buyer_performance.csv`, `variety_performance.csv` and `monthly_sales.csv`.

Suggested pages:
1. Executive overview: revenue, operating contribution, harvested kg, wastage %, collection %; revenue by season.
2. Season trends: revenue and operating contribution over time.
3. Buyer performance: revenue, revenue share, collections and outstanding balance.
4. Variety performance: quantity, revenue and average selling price.
5. Harvest and waste: harvested, rejected and saleable kg; import `data/raw/harvest.csv`.

Starter DAX measures (table names may need to match your model):
```DAX
Total Revenue = SUM(seasonal_kpis[revenue])
Operating Contribution = SUM(seasonal_kpis[operating_contribution])
Harvested KG = SUM(seasonal_kpis[harvested_kg])
Rejected KG = SUM(seasonal_kpis[rejected_kg])
Wastage Rate = DIVIDE([Rejected KG], [Harvested KG], 0)
```
Add a visible note: “Synthetic portfolio dataset — not actual business records.”
