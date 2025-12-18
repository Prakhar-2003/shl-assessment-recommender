import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vectorstore/faiss.index")

with open("vectorstore/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def retrieve(query, k=15):
    q_emb = model.encode([query])
    _, idxs = index.search(q_emb, k)

    results = []
    for i in idxs[0]:
        results.append(metadata[i])

    return results
