# Enterprise-Knowledge-Assistant


## Overview

Enterprise Knowledge Assistant is a production-oriented AI knowledge management platform being built to help organizations securely upload, manage, search, and interact with internal documents using Retrieval-Augmented Generation (RAG).

Week 1 focused on building the core backend infrastructure required for scalable AI applications.

---

## Week 1 Objectives

* Setup FastAPI backend
* Configure PostgreSQL database
* Implement JWT Authentication
* Setup SQLAlchemy ORM
* Configure Alembic migrations
* Dockerize the application
* Setup Docker Compose environment
* Establish clean project architecture

---

## Tech Stack

### Backend

* Python 3.11
* FastAPI
* SQLAlchemy
* Pydantic

### Database

* PostgreSQL 16
* Alembic

### Authentication

* JWT Tokens
* Password Hashing

### DevOps

* Docker
* Docker Compose

---

## Features Implemented

### User Authentication

#### Register User

```http
POST /register
```

Create a new user account.

#### Login

```http
POST /login
```

Authenticate user and generate JWT token.

#### Current User

```http
GET /me
```

Returns currently authenticated user details.

---

### Database Integration

Implemented:

* PostgreSQL Connection
* SQLAlchemy ORM Models
* Session Management
* Dependency Injection

---

### Database Migration System

Implemented Alembic for:

* Schema Versioning
* Database Migrations
* Production Database Management

Current Migration:

```text
initial_schema
```

Creates:

```sql
users
```

table with:

```sql
id
email
password_hash
role
created_at
```

---

### Docker Support

Application can be started using:

```bash
docker compose up --build
```

Containers:

```text
ka_api
ka_postgres
```

---

## Project Structure

```text
backend/

├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   │
│   ├── api/
│   │   └── auth.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── jwt_utils.py
│   │   └── security.py
│   │
│   ├── models/
│   │   └── users.py
│   │
│   ├── schemas/
│   │   └── users.py
│   │
│   ├── db.py
│   └── main.py
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## Environment Variables

```env
DATABASE_URL=postgresql://postgres:password@db:5432/knowledge_assistant

JWT_SECRET=your_secret_key

JWT_ALGORITHM=HS256
```

---

## Running the Project

### Clone Repository

```bash
git clone <repository-url>
cd backend
```

### Start Application

```bash
docker compose up --build
```

### Access API Documentation

```text
http://localhost:8000/docs
```

---

## API Endpoints

### Authentication

| Method | Endpoint  | Description  |
| ------ | --------- | ------------ |
| POST   | /register | Create User  |
| POST   | /login    | User Login   |
| GET    | /me       | Current User |

---

## Week 1 Deliverables Completed

* FastAPI Backend Setup
* PostgreSQL Integration
* JWT Authentication
* Password Hashing
* SQLAlchemy ORM
* Alembic Migration System
* Docker Configuration
* Docker Compose Setup
* Clean Project Structure
* Swagger Documentation

---

### Current Status

**Week 1 Complete ✅**

Infrastructure foundation established and ready for document ingestion and RAG implementation in Week 2.

---

# Week 2 - Document Ingestion Pipeline

Week 2 focused on building the complete document ingestion pipeline required before implementing Retrieval-Augmented Generation (RAG). The application can now upload documents, process PDF content, clean extracted text, generate chunks, and persist them in PostgreSQL.

---

## Week 2 Objectives

* Build Document Management Module
* Implement PDF Upload API
* Design Document Database Model
* Extract Text from PDF Files
* Build Text Cleaning Pipeline
* Generate Text Chunks
* Store Chunks in PostgreSQL
* Create Modular Service Layer
* Prepare Backend for Embedding Generation

---

## Features Implemented

### Document Management

Implemented a dedicated document module.

Features:

* Document Upload
* Document Metadata Storage
* User Ownership
* Upload Timestamp
* File Path Management

Database Model:

```text
Documents

id
filename
filepath
uploaded_by
created_at
```

Relationship:

```text
User
   │
   └──────────► Documents
```

---

### PDF Processing

Created a dedicated PDF processing service using **PyMuPDF (fitz)**.

Capabilities:

* Open PDF Documents
* Read Multiple Pages
* Extract Complete Text
* Count Total Pages

---

### Text Cleaning Pipeline

Created a reusable preprocessing service.

Processing includes:

* Remove extra whitespace
* Remove blank lines
* Normalize extracted text
* Prepare content for chunk generation

---

### Text Chunking

Implemented a chunk generation service.

Current Features:

* Fixed-size chunk generation
* Modular chunking architecture
* Ready for overlap-based chunking

Purpose:

Prepare document content for semantic embeddings.

---

### Chunk Database

Created a dedicated Chunk model.

Database Structure:

```text
Documents
      │
      ▼
Chunks
```

Chunk Fields:

```text
id
document_id
chunk_index
content
created_at
```

Relationship:

```text
Document
      │
      └──────────► Chunks
```

---

### Chunk Storage

Implemented a dedicated database service responsible for storing generated chunks.

Responsibilities:

* Save all generated chunks
* Maintain document relationship
* Efficient single transaction commit

---

### Service Layer

Refactored the application into modular services.

Current Services:

```text
services/

document_service.py

pdf_service.py

text_cleaner.py

chunk_service.py

chunk_db_service.py

ingestion_service.py
```

Each service has a single responsibility, making the project easier to maintain and extend.

---

## Updated Project Structure

```text
backend/

├── app/
│   │
│   ├── api/
│   │   ├── auth.py
│   │   └── documents.py
│   │
│   ├── core/
│   │
│   ├── models/
│   │   ├── users.py
│   │   ├── document.py
│   │   └── chunk.py
│   │
│   ├── schemas/
│   │   ├── users.py
│   │   └── document.py
│   │
│   ├── services/
│   │   ├── document_service.py
│   │   ├── pdf_service.py
│   │   ├── text_cleaner.py
│   │   ├── chunk_service.py
│   │   ├── chunk_db_service.py
│   │   └── ingestion_service.py
│   │
│   ├── db.py
│   └── main.py
│
├── uploads/
├── alembic/
└── docker-compose.yml
```

---

## Document Processing Pipeline

```text
Upload PDF
      │
      ▼
Save File
      │
      ▼
Create Document Record
      │
      ▼
Extract PDF Text
      │
      ▼
Clean Text
      │
      ▼
Generate Chunks
      │
      ▼
Store Chunks
```

---

## Database Schema

```text
Users
   │
   ▼
Documents
   │
   ▼
Chunks
```

---

## New API Endpoints

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /documents/upload | Upload and process PDF documents |

---

## Week 2 Deliverables Completed

* Document Model
* Chunk Model
* User → Document Relationship
* Document → Chunk Relationship
* PDF Upload Pipeline
* PDF Text Extraction
* Text Cleaning
* Text Chunk Generation
* Chunk Storage
* Modular Service Layer
* Docker Development Improvements
* Database Migrations

---

## Current Status

**Week 2 Complete ✅**

The backend now supports end-to-end document ingestion. Uploaded PDF documents are processed into structured text chunks and stored in PostgreSQL, providing the foundation for semantic embeddings and Retrieval-Augmented Generation (RAG).

---

## Next Phase (Week 3)

Week 3 will focus on the AI layer by implementing:

* Sentence Transformer Embeddings
* pgvector Integration
* Vector Similarity Search
* Retrieval Pipeline
* LLM Integration
* Conversational RAG