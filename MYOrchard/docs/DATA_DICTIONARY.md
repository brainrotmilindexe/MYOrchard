# Data dictionary

All rows are synthetic and reproducibly generated with a fixed random seed.

| File | Row grain | Purpose |
|---|---|---|
| seasons.csv | One row per season | Season and scenario flags |
| buyers.csv | One row per fictional buyer | Buyer segment and market |
| varieties.csv | One row per mango variety | Variety and base-price assumptions |
| orchard_blocks.csv | One row per block | Fictional acreage |
| harvest.csv | Season × block × variety | Harvest, rejection and saleable kg |
| sales.csv | One row per invoice line | Quantity, price, discount, revenue and collection |
| expenses.csv | Season × expense category | Simplified simulated operating costs |

Revenue = quantity × price less discount. Saleable kg = harvested kg less rejected kg. Operating contribution = revenue less included simulated operating costs; it is not audited net profit.
