from fastapi import FastAPI
from app.retriever import retrieve
from app.reranker import rerank

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(payload: dict):
    query = payload["query"]
    retrieved = retrieve(query, 15)
    final = rerank(query, retrieved)

    return {
        "recommendations": [
            {
                "assessment_name": r["name"],
                "assessment_url": r["url"]
            } for r in final
        ]
    }
