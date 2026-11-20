"""Chegg adjusted-close stock price audit; output only when real data is supplied."""
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

def analyze(path: Path):
    df = pd.read_csv(path)
    df.columns = [str(x).strip() for x in df.columns]
    if not {"Date", "Close"}.issubset(df.columns):
        raise ValueError("Expected Date and Close columns (same adjustment basis)")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Date", "Close"]).sort_values("Date")
    df = df.loc[df.Close > 0].drop_duplicates("Date", keep="last")
    if len(df) < 2:
        raise ValueError("At least two distinct valid trading days required")
    peak = df.loc[df["Close"].idxmax()]
    end = df.iloc[-1]
    if peak.Date >= end.Date:
        raise ValueError("Maximum close is on last date; peak-to-end decline is not meaningful")
    summary = pd.DataFrame([{
        "peak_date": peak.Date.date().isoformat(),
        "peak_adjusted_close_usd": round(float(peak.Close), 6),
        "end_date": end.Date.date().isoformat(),
        "end_adjusted_close_usd": round(float(end.Close), 6),
        "peak_to_end_decline_pct": round((1 - float(end.Close)/float(peak.Close))*100, 3),
        "price_basis": "adjusted_close_required_verify_input",
    }])
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "chegg_stock_history.csv", index=False)
    summary.to_csv(OUT / "stock_decline_summary.csv", index=False)
    return summary

def download():
    import yfinance as yf
    data = yf.download("CHGG", start="2021-01-01", end="2026-11-21", auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError("No CHGG data downloaded; provide a CSV manually")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "downloaded_chgg_adjusted.csv"
    data.reset_index().to_csv(path, index=False)
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="?", type=Path)
    parser.add_argument("--download", action="store_true", help="Fetch adjusted CHGG close via Yahoo Finance")
    args = parser.parse_args()
    if args.download == bool(args.csv):
        parser.error("Provide exactly one: a CSV path OR --download")
    path = download() if args.download else args.csv
    print(analyze(path).to_string(index=False))
