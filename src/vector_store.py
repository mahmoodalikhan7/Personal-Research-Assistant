import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# load embedding model locally — no API call, free
model = SentenceTransformer("all-MiniLM-L6-v2")

# create a local chromadb client
client = chromadb.Client()

def store_and_retrieve(chunks: list, user_query: str, top_k: int = 12) -> list:
    # create a fresh collection each time
    collection_name = "research"
    
    # delete if already exists
    try:
        client.delete_collection(collection_name)
    except:
        pass

    collection = client.create_collection(collection_name)

    # embed all chunks
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts).tolist()

    # store in chromadb
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"url": chunk["url"], "title": chunk["title"]} for chunk in chunks],
        ids=[str(i) for i in range(len(chunks))]
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")

    # embed the user query and retrieve top_k chunks
    query_embedding = model.encode([user_query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    # format retrieved chunks
    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "url": results["metadatas"][0][i]["url"],
            "title": results["metadatas"][0][i]["title"]
        })

    return retrieved


# test it
if __name__ == "__main__":
    test_chunks = [
        {"text": "Amyloid plaques are a hallmark of Alzheimer's disease.", "url": "https://example.com", "title": "Test"},
        {"text": "Tau protein tangles disrupt brain cell communication.", "url": "https://example.com", "title": "Test"},
        {"text": "APOE4 gene increases risk of Alzheimer's significantly.", "url": "https://example.com", "title": "Test"},
        {"text": "Exercise may reduce the risk of cognitive decline.", "url": "https://example.com", "title": "Test"},
    ]

    query = "What causes Alzheimer's disease?"
    results = store_and_retrieve(test_chunks, query, top_k=2)

    print(f"\nTop retrieved chunks for: '{query}'")
    for r in results:
        print(f"\n→ {r['text']}")
        print(f"  Source: {r['url']}")
