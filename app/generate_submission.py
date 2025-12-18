import pandas as pd
from app.retriever import retrieve
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Gen_AI_Dataset.xlsx"
OUT_PATH = BASE_DIR / "data" / "submission.csv"

df = pd.read_excel(DATA_PATH)

rows = []
for q in df["Query"]:
    recs = retrieve(q, 10)
    for r in recs:
        rows.append([q, r["url"]])

pd.DataFrame(rows, columns=["Query", "Assessment_url"]) \
  .to_csv(OUT_PATH, index=False)

print("submission.csv generated")
