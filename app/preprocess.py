import json

INPUT = "data/shl_raw.json"
OUTPUT = "data/shl_processed.json"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

processed = []
for d in data:
    text = f"{d['name']} {d.get('description','')} {d.get('test_type','')}"
    processed.append({
        "name": d["name"],
        "url": d["url"],
        "test_type": d.get("test_type", "Unknown"),
        "text": text.strip()
    })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2)

print("Preprocessing done")
