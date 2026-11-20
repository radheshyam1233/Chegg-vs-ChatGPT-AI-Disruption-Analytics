"""ASSISTments observational SQL analytics from the *real* 2009-2010 Skill Builder CSV.

We intentionally do not synthesize learning results or imply causation.
"""
import argparse
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
REQUIRED = {"user_id", "order_id", "skill_id", "correct", "hint_count", "bottom_hint", "opportunity"}


def run(path: Path):
    data = pd.read_csv(path, encoding="ISO-8859-15", low_memory=False)
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df = data[list(REQUIRED)].copy()
    for col in ("order_id", "correct", "hint_count", "bottom_hint", "opportunity"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["skill_id"] = df["skill_id"].astype("string").str.strip()
    # A non-atomic skill list would double-count one interaction if exploded.
    multiple_skills = df["skill_id"].str.contains("[,;]", regex=True, na=False).sum()
    # User ID and skill ID define a student-skill cohort, not a unique person.
    audit = pd.DataFrame([{
        "source_rows": len(data),
        "unique_students": data.user_id.nunique(),
        "unique_order_ids": data.order_id.nunique(),
        "missing_skill_rows": int(df.skill_id.isna().sum()),
        "non_atomic_skill_rows": int(multiple_skills),
        "missing_opportunity_rows": int(df.opportunity.isna().sum()),
        "duplicate_student_skill_opportunities": int(df.dropna(subset=["skill_id", "opportunity"]).duplicated(["user_id", "skill_id", "opportunity"]).sum()),
        "invalid_correct_rows": int((~df.correct.isin([0, 1])).sum()),
    }])
    # Exclude invalid outcome / skill / ordering records and ambiguous multi-skill rows.
    eligible = df.loc[
        df.user_id.notna() & df.skill_id.notna() & (df.skill_id != "")
        & ~df.skill_id.str.contains("[,;]", regex=True, na=False)
        & df.order_id.notna() & df.opportunity.notna()
        & df.correct.isin([0, 1])
    ].copy()
    # Avoid repeated student-skill-opportunity ties that make sequencing arbitrary.
    eligible = eligible.sort_values(["user_id", "skill_id", "opportunity", "order_id"])
    eligible = eligible.drop_duplicates(["user_id", "skill_id", "opportunity"], keep="first")
    audit["eligible_rows_after_audit_rules"] = len(eligible)
    # Convert to non-NA objects for SQLite.
    eligible["skill_id"] = eligible["skill_id"].astype(str)
    with sqlite3.connect(":memory:") as con:
        eligible.to_sql("student_attempts", con, index=False, if_exists="replace")
        sql = (ROOT / "sql" / "02_learning_analytics.sql").read_text(encoding="utf-8")
        con.executescript(sql)
        outputs = {
            "assistments_help_groups.csv": "SELECT * FROM help_groups ORDER BY interactions DESC",
            "assistments_next_opportunity_accuracy.csv": "SELECT * FROM next_opportunity_accuracy ORDER BY help_group",
            "final_mastery_comparison.csv": "SELECT * FROM mastery_comparison ORDER BY help_group",
        }
        OUT.mkdir(parents=True, exist_ok=True)
        for filename, query in outputs.items():
            result = pd.read_sql_query(query, con)
            result.to_csv(OUT / filename, index=False)
            print("\n", filename, "\n", result.to_string(index=False))
    audit.to_csv(OUT / "assistments_data_audit.csv", index=False)
    print("\nAUDIT:\n", audit.to_string(index=False))
    return audit

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("csv", type=Path, help="Original downloaded ASSISTments Skill Builder CSV")
    args = cli.parse_args()
    run(args.csv)
