-- SQLite-compatible starter schema
CREATE TABLE seasons (season_id TEXT PRIMARY KEY, season TEXT, start_year INTEGER, pandemic_scenario INTEGER, market_pressure_scenario INTEGER, scenario_note TEXT);
CREATE TABLE buyers (buyer_id TEXT PRIMARY KEY, buyer_name TEXT, buyer_type TEXT, market TEXT);
CREATE TABLE varieties (variety_id TEXT PRIMARY KEY, variety TEXT, acre_share REAL, base_price_per_kg REAL);
CREATE TABLE sales (invoice_line_id TEXT PRIMARY KEY, invoice_date TEXT, season_id TEXT, buyer_id TEXT, variety_id TEXT, quantity_kg INTEGER, price_per_kg REAL, discount_amount REAL, revenue REAL, amount_collected REAL, payment_status TEXT, FOREIGN KEY(season_id) REFERENCES seasons(season_id), FOREIGN KEY(buyer_id) REFERENCES buyers(buyer_id), FOREIGN KEY(variety_id) REFERENCES varieties(variety_id));
-- CSVs for harvest and expenses are included in data/raw and can be imported as fact tables.
