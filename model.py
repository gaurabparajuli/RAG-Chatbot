import ollama
from embeddings import query_chroma

def generate_response(query, model="mistral:latest"):
    results = query_chroma(query)
    retrieved_docs = "\n\n".join(results["documents"][0])
    prompt = f"""You are an AI assistant. Use the following retrieved context to answer the user's question.

    Context:
    {retrieved_docs}

    Question: {query}
    
    Answer:"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"], retrieved_docs