# RAG-Based Document Intelligence Platform

A production-ready Retrieval-Augmented Generation (RAG) backend platform that enables users to upload documents, generate vector embeddings, perform semantic search, and ask context-aware questions using OpenAI Large Language Models.

The system is designed using FastAPI, PostgreSQL, pgvector, Redis, Celery, Docker, and OpenAI APIs following real-world backend architecture practices.

---

## Features

### Authentication & Security

- User Signup and Login
- JWT Authentication
- Protected APIs
- User-specific document access control

### Document Management

- PDF Upload
- Document ownership validation
- Document deletion
- Processing status tracking

### RAG Pipeline

- PDF text extraction
- Intelligent text chunking
- OpenAI embedding generation
- Vector storage using pgvector
- Semantic similarity search
- Context-aware answer generation

### Chat System

- Ask questions about uploaded documents
- Chat history storage
- Document-specific conversations

### Production Features

- Background processing with Celery
- Redis task broker
- Structured logging
- Health check endpoints
- Pagination support
- Global exception handling
- Standardized API responses
- Dockerized deployment

---

## System Architecture

### High-Level Flow

```text
Client
   │
   ▼
FastAPI Backend
   │
   ├── Authentication APIs
   ├── Document APIs
   ├── Chat APIs
   └── Dashboard APIs
   │
   ▼
PostgreSQL + pgvector
   │
   ├── Users
   ├── Documents
   ├── Document Embeddings
   └── Chats
   │
   ▼
OpenAI APIs
```

### Document Processing Pipeline

```text
PDF Upload
    │
    ▼
Celery Worker
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
OpenAI Embeddings
    │
    ▼
pgvector Storage
```

### Question Answering Flow

```text
User Question
      │
      ▼
Generate Question Embedding
      │
      ▼
pgvector Similarity Search
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
OpenAI LLM
      │
      ▼
Context-Aware Answer
```

---

## Tech Stack

| Layer | Technology |
|---------|---------|
| Backend | FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT |
| AI/LLM | OpenAI |
| Background Jobs | Celery |
| Broker | Redis |
| Containerization | Docker |

---

## Database Design

### Users

```text
id
email
password_hash
created_at
```

### Documents

```text
id
user_id
filename
file_path
processing_status
upload_time
```

### Document Embeddings

```text
id
document_id
chunk_text
embedding
```

### Chats

```text
id
user_id
document_id
question
answer
created_at
```

---

## API Endpoints

### Authentication

```http
POST /auth/signup
POST /auth/login
```

### Documents

```http
POST   /documents/upload
GET    /documents
DELETE /documents/{id}
```

### Chat

```http
POST /chat/ask
GET  /chat/history
```

### Dashboard

```http
GET /dashboard/summary
```

### Health Checks

```http
GET /health
GET /health/db
GET /health/redis
```

---

## Environment Variables

Create a `.env` file using:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

DATABASE_URL=

SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

OPENAI_API_KEY=

REDIS_URL=
```

---

## Local Development Setup

### Clone Repository

```bash
git clone https://github.com/amirthasriomraj/rag-document-chatbot-backend.git

cd rag-document-chatbot-backend
```

### Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Docker Setup

### Start Services

```bash
docker compose up --build
```

### Services

| Service | Port |
|---------|---------|
| FastAPI | 8001 |
| PostgreSQL | 5433 |
| Redis | 6380 |

### API Documentation

```text
http://localhost:8001/docs
```

---

## Example Workflow

```text
1. User uploads a PDF document
2. Celery worker processes the file
3. Text is extracted and chunked
4. OpenAI embeddings are generated
5. Embeddings are stored in PostgreSQL using pgvector
6. User asks a question
7. Relevant chunks are retrieved using vector similarity search
8. Context is sent to OpenAI
9. Answer is generated
10. Chat history is stored
```

---

## Production Features Implemented

- JWT Authentication
- User Ownership Validation
- Background Task Processing
- Vector Similarity Search
- Chat History Tracking
- Structured Logging
- Global Exception Handling
- Health Monitoring
- Pagination
- Standard API Responses
- Dockerized Deployment

---

## Future Improvements

- Multi-document retrieval
- Hybrid search (keyword + vector)
- Streaming responses
- Source citations
- Role-based access control
- Kubernetes deployment
- Observability dashboards
