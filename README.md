# Chegg vs ChatGPT — AI Disruption & Learning Analytics


## 🚀 Live Dashboard

[**View the Interactive Chegg vs ChatGPT Analytics Dashboard**](https://radheshyam1233-chegg-vs-chatgpt-ai-disrupti-appdashboard-zn7rsb.streamlit.app/)

Explore three sections: Chegg financial disruption, ASSISTments student learning analytics, and stock performance with market-sizing scenarios.


**SQL · Python · Power BI · Data Analytics · Business Strategy**

A three-part reproducible portfolio analyzing (1) Chegg financial disruption, (2) learning effects associated with hints in ASSISTments, and (3) equity performance and an AI-first Indian test-prep product scenario.

## Evidence and honest scope

| Area | Status |
|---|---|
| Financial | Working quarterly values: Q4 2022 to Q4 2024 revenue **-30.07%**, subscribers **-27.38%**; pending individual-line reconciliation against issuer reports. |
| ASSISTments | Complete runnable hint/mastery analytics, requires original 2009–2010 corrected Skill Builder CSV. **No student performance results fabricated.** |
| Stock | Adjusted historical close downloader and peak-to-end decline calculation. The result depends on the retrieved series and dates; **do not assert 99% without an audited run**. |
| Market | ₹2,000 crore modeled *annual opportunity* (10M potential learners × ₹2,000 annual spend), **not a published industry TAM**. |
| Dashboards | Working Streamlit source + Power BI build instructions and DAX. Actual Power BI `.pbix` requires export from Power BI Desktop. |

## Quick start

Python 3.10+ recommended. From project root:

```bash
python -m pip install -r requirements.txt
python scripts/run_financial.py
python scripts/run_market.py
streamlit run app/dashboard.py
```

To add the two actual external-source datasets:

```bash
python scripts/run_learning.py path/to/skill_builder_data_corrected_collapsed.csv
python scripts/run_stock.py --download
# Or: python scripts/run_stock.py path/to/adjusted_CHGG_price_history.csv
```

To run code tests with **synthetic test-only fixtures**:

```bash
python -m pytest tests -q
```

### Portfolio components

- **Financial analysis:** `sql/01_financial_analysis.sql`, `scripts/run_financial.py`, `data/chegg_financials_working.csv`.
- **Learning analytics:** `sql/02_learning_analytics.sql`, `scripts/run_learning.py`. Uses `LAG`, `LEAD`, cohort classification, SQL joins, and operational mastery (three consecutive correct first responses).
- **Stock:** `scripts/run_stock.py` downloads historical adjusted CHGG close (requires network access), or accepts user-supplied adjusted-price CSV.
- **Market scenarios:** `scripts/run_market.py` generates conservative/base/optimistic revenue opportunity models in INR crore.
- **Dashboard:** `app/dashboard.py` (runnable Streamlit companion), `powerbi/` (Power BI build guide/DAX).
- **Strategy:** `docs/strategy_memo.md`, `docs/SOURCES_AND_AUDIT.md`.

## Methodology cautions

- **Associations, not causation:** Chegg financial trends after ChatGPT's release do not isolate the impact of AI.
- **ASSISTments:** `correct` is correctness on initial problem response and often precedes hints; final/bottom hint is not a randomized direct-answer intervention. Right-censoring, baseline skill and problem difficulty may explain observed differences.
- **Mastery proxy:** three consecutive correct responses for a student-skill, not validated durable knowledge.
- **Stock:** dates and corporate actions matter; record adjustment basis.
- **Market:** scenario assumptions require validation through independent research.

## External research sources

- [Chegg 2024 annual 10-K](https://www.sec.gov/Archives/edgar/data/1364954/000136495425000013/chgg-20241231.htm)
- [Chegg Q4 2024 investor data sheet](https://s21.q4cdn.com/596622263/files/doc_financials/2024/q4/Q4-24-Chegg-Data-Sheet-Final.pdf)
- [ASSISTments 2009–2010 corrected Skill Builder data](https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data/skill-builder-data-2009-2010)

See `docs/POWERBI_AND_PUBLICATION.md` for finishing the actual report.
