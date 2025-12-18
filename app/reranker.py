import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def rerank(query, candidates):
    prompt = f"""
    Query: {query}

    Rank the following assessments from most relevant to least relevant.
    Return only the top 10 names.

    {chr(10).join([c['name'] for c in candidates])}
    """

    response = model.generate_content(prompt)

    ranked = []
    for line in response.text.split("\n"):
        for c in candidates:
            if line.lower() in c["name"].lower():
                ranked.append(c)

    return ranked[:10]

