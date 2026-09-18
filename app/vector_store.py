import os
import chromadb
from chromadb.utils import embedding_functions

# Define the local storage path for the persistent vector database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db")

# Initialize the persistent client
chroma_client = chromadb.PersistentClient(path=DB_PATH)

# Initialize the open-source embedding model 
# (This will automatically download the lightweight model on the first run)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def get_collection():
    """
    Retrieve or create the ChromaDB collection for document storage.
    """
    return chroma_client.get_or_create_collection(
        name="docusense_policies",
        embedding_function=embedding_fn
    )

def build_vector_store(chunks: list) -> None:
    """
    Convert text chunks into vector embeddings and index them in the database.
    """
    collection = get_collection()
    
    # Clear existing data to avoid duplicate entries during repeated local testing
    if collection.count() > 0:
        existing_data = collection.get()
        if existing_data['ids']:
            collection.delete(ids=existing_data['ids'])
    
    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    
    # Add the documents. Chroma automatically computes the embeddings using the embedding_fn.
    collection.add(
        documents=documents,
        ids=ids
    )
    print(f"Successfully indexed {len(documents)} chunks into the vector store.")

def retrieve_context(query: str, top_k: int = 3) -> dict:
    """
    Query the vector store for the most semantically similar chunks to the user's question.
    """
    collection = get_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    return results

if __name__ == "__main__":
    from document_processor import load_document, chunk_text
    
    # 1. Process the document using Phase 2 logic
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(base_dir, "..", "data", "company_policies.md")
    
    raw_content = load_document(source_file)
    processed_chunks = chunk_text(raw_content, chunk_size=400, overlap=50)
    
    # 2. Build the vector index
    print("Building vector index...")
    build_vector_store(processed_chunks)
    
    # 3. Test the retrieval pipeline with the required assessment question
    test_query = "What is the policy on database backup retention periods?"
    print(f"\nSearching for: '{test_query}'\n")
    
    search_results = retrieve_context(test_query, top_k=2)
    
    print("Top 2 Retrieved Chunks:")
    for i in range(len(search_results['ids'][0])):
        print(f"ID: {search_results['ids'][0][i]}")
        print(f"Distance: {search_results['distances'][0][i]:.4f}")
        print(f"Text: {search_results['documents'][0][i]}")
        print("-" * 50)