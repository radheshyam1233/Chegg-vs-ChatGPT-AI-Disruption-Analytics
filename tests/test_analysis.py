"""Synthetic fixtures test code only. They are NOT reported research findings."""
import tempfile
from pathlib import Path
import pandas as pd
from scripts.run_stock import analyze
from scripts.run_learning import run

def test_stock_decline_from_input():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "prices.csv"
        pd.DataFrame({"Date": ["2021-01-01", "2021-01-02", "2021-01-03"], "Close": [100,80,20]}).to_csv(path,index=False)
        result = analyze(path)
        assert result.peak_to_end_decline_pct.iloc[0] == 80.0

def test_learning_pipeline():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "toy.csv"
        pd.DataFrame({"user_id": [1]*4+[2]*4,
            "skill_id": [10]*8,"order_id": list(range(1,9)),
            "opportunity": [1,2,3,4]*2,"correct": [0,1,1,1,0,0,1,0],
            "hint_count": [1,0,0,0,2,1,0,0],
            "bottom_hint": [0,0,0,0,1,0,0,0]}).to_csv(path,index=False)
        audit = run(path)
        assert audit.source_rows.iloc[0] == 8
        result = pd.read_csv(Path(__file__).resolve().parents[1]/"outputs/final_mastery_comparison.csv")
        guided = result.loc[result.help_group=="Guided Hints"].iloc[0]
        assert guided.mastered_pairs == 1
        assert guided.mastery_rate_pct == 100.0
