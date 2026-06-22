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
