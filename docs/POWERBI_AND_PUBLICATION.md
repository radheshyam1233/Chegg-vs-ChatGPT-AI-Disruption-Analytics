# Publishing and Power BI completion

1. Run the financial and market scripts to produce the bundled CSVs.
2. Download the original corrected ASSISTments Skill Builder CSV from the dataset owner. Run the learning script and inspect `outputs/assistments_data_audit.csv`. Do not claim outputs that are absent.
3. Run the stock script with a sourced adjusted-close series or its `--download` option. Record data retrieval date and corporate-action adjustment basis.
4. Power BI Desktop: import `outputs/financial_powerbi.csv`, `outputs/final_mastery_comparison.csv` (if generated), `outputs/assistments_help_groups.csv`, `outputs/assistments_next_opportunity_accuracy.csv`, `outputs/chegg_stock_history.csv` and `outputs/india_testprep_market_scenarios.csv`. Follow `powerbi/BUILD_GUIDE.md` and `powerbi/DAX_measures.txt`.
5. Save the real `.pbix` from Power BI Desktop and optionally export screenshots and PDF. This source project does **not** create a fake binary report.
6. For a browser-accessible three-page companion dashboard, run `streamlit run app/dashboard.py`.
7. Do not upload source student records if the dataset license or privacy terms prohibit redistribution. Prefer official download instructions.
