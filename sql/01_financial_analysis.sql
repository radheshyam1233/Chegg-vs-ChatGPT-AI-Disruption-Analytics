-- Run after loading data/chegg_financials_working.csv into chegg_financials.
SELECT quarter, revenue_million, subscribers,
 LAG(revenue_million,4) OVER (ORDER BY quarter) AS revenue_year_ago,
 ROUND(100.0*(revenue_million/LAG(revenue_million,4) OVER (ORDER BY quarter)-1),2) AS yoy_revenue_pct
FROM chegg_financials ORDER BY quarter;

SELECT ROUND(100.0*(a.revenue_million-b.revenue_million)/a.revenue_million,2) AS revenue_decline_pct,
 ROUND(100.0*(a.subscribers-b.subscribers)/a.subscribers,2) AS subscriber_decline_pct
FROM chegg_financials a JOIN chegg_financials b
ON a.quarter='2022-Q4' AND b.quarter='2024-Q4';
