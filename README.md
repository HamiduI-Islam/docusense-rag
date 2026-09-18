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

### 5. Test the Application
The application features a built-in Swagger UI for interactive testing.
1. Open your web browser and navigate to: `http://localhost:8000/docs`
2. Expand the **POST /api/query** endpoint and click **Try it out**.
3. Submit the following JSON payload:
```json
{
  "question": "What are the primary key points discussed in the document?"
}
```
4. Click **Execute** to view the `200 OK` response containing the LLM's grounded answer and the specific document chunks used for context.

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