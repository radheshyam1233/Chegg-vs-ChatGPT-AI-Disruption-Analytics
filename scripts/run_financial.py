from pathlib import Path
import sqlite3, pandas as pd
root=Path(__file__).resolve().parents[1]
df=pd.read_csv(root/'data/chegg_financials_working.csv')
con=sqlite3.connect(':memory:')
df.to_sql('chegg_financials',con,index=False)
sql=(root/'sql/01_financial_analysis.sql').read_text()
for stmt in sql.split(';'):
 if stmt.strip():
  print(pd.read_sql_query(stmt,con).to_string(index=False))
(root/'outputs').mkdir(exist_ok=True)
df.to_csv(root/'outputs/financial_powerbi.csv',index=False)
