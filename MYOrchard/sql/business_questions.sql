-- Revenue by season
SELECT se.season, ROUND(SUM(s.revenue),2) AS revenue
FROM sales s JOIN seasons se ON s.season_id=se.season_id
GROUP BY se.season_id,se.season ORDER BY se.start_year;

-- Top buyers
SELECT b.buyer_name, b.market, ROUND(SUM(s.revenue),2) AS revenue
FROM sales s JOIN buyers b ON s.buyer_id=b.buyer_id
GROUP BY b.buyer_id,b.buyer_name,b.market ORDER BY revenue DESC;

-- Variety performance
SELECT v.variety, SUM(s.quantity_kg) AS quantity_kg, ROUND(SUM(s.revenue),2) AS revenue
FROM sales s JOIN varieties v ON s.variety_id=v.variety_id
GROUP BY v.variety_id,v.variety ORDER BY revenue DESC;

-- Outstanding balances
SELECT b.buyer_name, ROUND(SUM(s.revenue-s.amount_collected),2) AS outstanding
FROM sales s JOIN buyers b ON s.buyer_id=b.buyer_id
GROUP BY b.buyer_id,b.buyer_name ORDER BY outstanding DESC;
