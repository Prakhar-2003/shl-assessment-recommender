import pandas as pd
from app.retriever import retrieve
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Gen_AI_Dataset.xlsx"

df = pd.read_excel(DATA_PATH)

hits = 0
for _, row in df.iterrows():
    query = row["Query"]
    true_url = row["Assessment_url"]

    preds = retrieve(query, 10)
    urls = [p["url"] for p in preds]

    if true_url in urls:
        hits += 1

print("Final Recall@10:", hits / len(df))

