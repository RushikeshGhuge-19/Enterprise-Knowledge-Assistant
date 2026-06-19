# Enterprise Knowledge Assistant - Backend (Week 1)

Complete FastAPI + PostgreSQL + Auth scaffold ready for Week 2 RAG integration.

## Architecture

```
FastAPI (Port 8000)
├── Auth Endpoints (JWT)
│   ├── POST /auth/signup → register user
│   ├── POST /auth/login → get token
│   └── GET /auth/me → get current user (protected)
├── Health Check
│   └── GET /health → server status
└── PostgreSQL (Port 5432)
    └── Users table (email, password_hash, role, created_at)
```

## Quick Start

### 1. Clone & Install

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Update .env

```bash
# .env
DATABASE_URL=postgresql://knowledge_user:knowledge_password@localhost:5432/knowledge_assistant
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
DEBUG=False
```

### 3. Start PostgreSQL with Docker

```bash
docker-compose up -d
```

Verify:
```bash
docker-compose ps
# Should show: postgres running on 5432, qdrant running on 6333
```

### 4. Run Migrations

```bash
# Create tables in database
alembic upgrade head
```

### 5. Run FastAPI Server

```bash
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

Docs at: `http://localhost:8000/docs`

---

## Testing Week 1

### Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status": "ok"}
```

### Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

Expected:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

Expected:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}
```

### Get Current User (Protected)

```bash
# Replace TOKEN with actual token from signup/login response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

Expected:
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00+00:00"
}
```

---

## Directory Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── db.py                   # SQLAlchemy setup
├── config.py               # Settings from .env
├── security.py             # Password hashing (bcrypt)
├── jwt_utils.py            # JWT token creation/validation
├── auth.py                 # Auth endpoints (signup, login, me)
├── users.py                # User SQLAlchemy model
├── user_schemas.py         # Pydantic schemas
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore
├── docker-compose.yml      # PostgreSQL + Qdrant
├── Dockerfile              # Production image
├── alembic.ini             # Alembic config
├── alembic/
│   ├── env.py              # Alembic environment
│   └── versions/
│       └── 001_create_users_table.py
└── venv/                   # Virtual environment
```

---

## Deployment to Railway

### 1. Create Railway Account & Project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init
```

### 2. Add PostgreSQL

```bash
# In Railway dashboard:
# - Add Database → PostgreSQL
# - Copy DATABASE_URL from PostgreSQL service variables
```

### 3. Set Environment Variables

```bash
railway variable set DATABASE_URL="postgresql://..."
railway variable set JWT_SECRET="your-production-secret-key"
railway variable set JWT_ALGORITHM="HS256"
railway variable set JWT_EXPIRE_MINUTES="30"
railway variable set DEBUG="False"
```

### 4. Deploy

```bash
# Deploy from current directory
railway up

# View logs
railway logs -f
```

### 5. Test on Railway

```bash
# Get your Railway URL
railway logs

# Test health check
curl https://your-railway-url.up.railway.app/health
```

---

## Interview Talking Points

**Q: Why JWT?**
> Stateless authentication. No session storage. Scalable across multiple servers. Industry standard. Token expires automatically.

**Q: Why bcrypt?**
> Slow by design (12 rounds). Resistant to brute force. Adaptive: if computers get faster, just increase rounds.

**Q: Why separate auth and data?**
> Clean separation of concerns. Auth validates credentials. Data layer handles queries. Easy to test, modify, extend.

**Q: Password storage?**
> Never store plaintext. Hash with bcrypt. Compare hashes, never original passwords. Each password has unique salt.

**Q: How does the token work?**
> User signs up → password hashed → stored in DB. User logs in → password verified → JWT generated with user_id. Client stores token → sends in Authorization header on protected requests → server verifies signature and expiry.

---

## Next Steps (Week 2)

After Week 1 is complete and tested:

1. **Document Model** → Add documents table, file uploads
2. **Text Extraction** → PDF/DOCX parsing with pdfplumber, python-docx
3. **Chunking** → Break documents into embeddings-friendly chunks
4. **Vector Storage** → Qdrant integration for semantic search
5. **RAG Chat** → LLM integration + retrieval chains

---

## Troubleshooting

### "connection refused" on PostgreSQL
```bash
# Check if containers are running
docker-compose ps

# Restart containers
docker-compose down
docker-compose up -d
```

### "DATABASE_URL not set"
```bash
# Make sure .env exists and is readable
ls -la .env
cat .env
```

### JWT Token Invalid
- Check JWT_SECRET in .env matches what's in code
- Verify token hasn't expired (default 30 min)
- Check Authorization header format: `Bearer <token>`

### Alembic Migration Failed
```bash
# Reset database (local only!)
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

---

## Tech Stack

- **Framework**: FastAPI 0.104
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Auth**: JWT + bcrypt
- **Migrations**: Alembic
- **Server**: Uvicorn
- **Containerization**: Docker + Compose

---

**Week 1 Complete. Ready for RAG integration in Week 2.**
