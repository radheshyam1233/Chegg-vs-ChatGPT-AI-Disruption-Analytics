# Power BI report build guide
1. Run `python scripts/run_financial.py` and `python scripts/run_market.py`.
2. Import `outputs/financial_powerbi.csv` and `outputs/india_testprep_market_scenarios.csv` as tables CheggFinancials and MarketScenarios.
3. Add DAX from `DAX_measures.txt`. Set percentage formatting.
4. Page 1: cards for revenue/subscriber decline; quarterly line charts for revenue and subscribers.
5. After running learning analysis on actual data, import `outputs/final_mastery_comparison.csv`. Page 2: mastery rate and opportunity bar charts by help_group; disclose observational limitations.
6. After running stock analysis on a sourced adjusted-price CSV, import it. Page 3: stock close by date, peak-to-end price decline with dates, scenario opportunity by market scenario, pivot recommendations.
7. Save `Chegg_AI_Disruption_Dashboard.pbix` locally. This repo does not include a fabricated `.pbix` file.
