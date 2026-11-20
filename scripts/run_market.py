from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[1]
df=pd.DataFrame({'scenario':['Conservative','Base','Optimistic'],'learners':[5000000,10000000,15000000],'annual_spend_inr':[1500,2000,2500],'capture_rate':[0.02,0.05,0.08]})
df['opportunity_crore']=df.learners*df.annual_spend_inr/10000000
df['captured_revenue_crore']=df.opportunity_crore*df.capture_rate
(root/'outputs').mkdir(exist_ok=True)
df.to_csv(root/'outputs/india_testprep_market_scenarios.csv',index=False)
print(df.to_string(index=False))
