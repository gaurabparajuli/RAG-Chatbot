import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="sentence_chunks")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def store_embeddings(text):
    chunks = split_text(text)
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk]
        )
    print(f"Stored {len(chunks)} chunks in vector database.")

def query_chroma(query_text, top_k=5):
    query_embedding = embedding_model.encode(query_text).tolist()
    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    # Read text from data.txt 
    with open("data.txt","r",encoding="utf-8")as file:
        text = file.read()

    store_embeddings(text)