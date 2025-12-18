import json, pickle, faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/shl_processed.json", "r") as f:
    data = json.load(f)

texts = [d["text"] for d in data]
embeddings = model.encode(texts, show_progress_bar=True)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

faiss.write_index(index, "vectorstore/faiss.index")

with open("vectorstore/metadata.pkl", "wb") as f:
    pickle.dump(data, f)

print("Embeddings + FAISS created")
