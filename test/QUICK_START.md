# Quick Start - 5 Minutes to Running

## Prerequisites
- Python 3.10+
- Docker & Docker Compose
- pip

## Go (Copy & Paste)

```bash
# 1. Setup virtual environment (1 min)
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies (2 min)
pip install -r requirements.txt

# 3. Configure (30 seconds)
cp .env.example .env

# 4. Start database (1 min)
docker-compose up -d
sleep 10  # Wait for PostgreSQL

# 5. Run migrations (30 seconds)
alembic upgrade head

# 6. Start server (30 seconds)
python -m uvicorn main:app --reload
```

**Server ready at: http://localhost:8000**
**Docs at: http://localhost:8000/docs**

---

## Test It

### In another terminal:

```bash
# Signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Copy the access_token from response, then:

TOKEN="paste_token_here"
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Done! You have a working backend.**

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `connection refused` | `docker-compose logs postgres` |
| `DATABASE_URL not set` | Check `.env` exists |
| Port 5432 in use | Change `docker-compose.yml` port |
| `alembic: command not found` | Run `pip install -r requirements.txt` again |

---

## Next: Deploy

When ready to deploy to Railway, see `RAILWAY_DEPLOY.md`.
