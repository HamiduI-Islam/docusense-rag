# 🧠 DocuSense: RAG Microservice

DocuSense is a containerized Retrieval-Augmented Generation (RAG) microservice. It securely processes documents, vectorizes their contents, and leverages advanced Large Language Models (LLMs) to provide accurate, grounded answers to user queries while strictly preventing hallucinations.

To ensure a frictionless evaluation, this project has been fully containerized. No local Python environments or dependency installations are required.

## ⚙️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | FastAPI | High-performance asynchronous API framework |
| **LLM Inference** | Groq API | Ultra-fast language model processing |
| **Vector Database**| ChromaDB | Local vector store for document embeddings |
| **Embeddings** | sentence-transformers | CPU-optimized PyTorch context vectorization |
| **Deployment** | Docker & Compose | Isolated, reproducible environment execution |

### 📐 Chunking & Embedding Strategy
* **Chunking Strategy:** Documents are processed using Recursive Character Splitting (~400 characters, 50-character overlap). **Justification:** This respects natural semantic boundaries (sentences/paragraphs) while the overlap ensures critical context is not lost across chunk edges, maintaining high retrieval accuracy.
* **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`. **Justification:** This model provides an optimal balance between semantic precision and resource efficiency. It is highly optimized for CPU inference, allowing the Docker container to generate dense vectors quickly without requiring GPU acceleration.
---

## 🚀 Quick Start Guide

Follow these exact steps to launch the microservice and test the API.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/docusense-rag.git](https://github.com/your-username/docusense-rag.git)
cd docusense-rag
```

### 2. Configure the Environment
For security, the API key is not committed to version control. 
* Locate the `.env.example` file in the root directory.
* Create a new file named exactly `.env` in the same location.
* Add your Groq API key (without quotes or spaces):
```text
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Build and Launch the Container
Start the Docker engine in the background, then execute the following command to build the image and start the Uvicorn server on port 8000.
```bash
docker compose up --build
```
*(Wait until the terminal displays `Application startup complete`.)*

### 4. Initialize the Vector Database
Open a **second, separate terminal window** while the server is running. Execute the following command to securely enter the active container and run the data ingestion script. This splits the document and stores the embeddings in ChromaDB:
```bash
docker compose exec docusense-api python app/vector_store.py
```

### 5. Verify & Test via Swagger UI
Open your browser and navigate to `http://localhost:8000/docs`. Under **POST /api/query**, click **Try it out** and test both scenarios:

#### Test Case 1: Grounded Information Retrieval
Submit an in-domain question:
```json
{
  "question": "What is the policy on database backup retention periods?"
}
```
*Expected Result:* `200 OK` response with the policy details retrieved from the document and listed context chunks.

#### Test Case 2: Anti-Hallucination Guardrail Check
Submit an out-of-scope question:
```json
{
  "question": "What are the ingredients needed to bake a chocolate cake?"
}
```
*Expected Result:* `200 OK` with a clear fallback rejection stating that the provided context does not contain relevant information, verifying zero model hallucination.

### 6. API Testing via cURL (Terminal)
Alternatively, you can test the API directly from your local terminal using the following curl commands. *(Note: These commands are formatted for Windows PowerShell/Command Prompt to safely escape JSON quotation marks).*

**Test Case A: High-Confidence Retrieval**
Verify the RAG system accurately extracts and answers based on the ingested document.
```bash
cmd.exe /c 'curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d "{\"question\": \"What is the policy on database backup retention periods?\"}"'
```
*Expected Result:* A `200 OK` JSON response containing the exact policy details retrieved from the document and the listed context chunks.

**Test Case B: Out-of-Scope Fallback Test**
Verify the system's guardrails successfully reject queries unrelated to the ingested data.
```bash
cmd.exe /c 'curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d "{\"question\": \"What are the ingredients needed to bake a chocolate cake?\"}"'
```
*Expected Result:* A `200 OK` JSON response featuring a clear fallback statement (e.g., "The provided context does not contain relevant information"), proving zero model hallucination.
```
---

## 📂 Project Structure

```text
docusense-rag/
├── app/
│   ├── document_processor.py   # Document parsing and chunking logic
│   ├── llm_service.py          # Groq API integration and prompt engineering
│   ├── main.py                 # FastAPI application and route definitions
│   └── vector_store.py         # ChromaDB ingestion and semantic search
├── data/
│   └── company_policies.md     # Source document for RAG ingestion
├── .env.example                # Template for required environment variables
├── docker-compose.yml          # Multi-container orchestration instructions
├── Dockerfile                  # Container build instructions (CPU optimized)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🧹 Teardown
To gracefully stop the application and clean up the Docker network, return to the first terminal and run:
```bash
docker compose down
```

---
**Author:** Hamidul Islam
