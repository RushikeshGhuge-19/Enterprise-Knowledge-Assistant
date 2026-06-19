# Week 1 Execution Checklist

Complete this by end of Friday.

---

## Day 1-2: Init (4 hours)

### File Structure
- [x] Create `backend/` directory
- [x] Create `app/` subdirectory
- [x] Create `app/api/`, `app/core/`, `app/models/`, `app/schemas/`

### Core Files
- [x] `main.py` - FastAPI entry point
- [x] `config.py` - Load .env settings
- [x] `db.py` - SQLAlchemy engine + session
- [x] `security.py` - bcrypt hash/verify
- [x] `jwt_utils.py` - JWT creation/validation
- [x] `users.py` - User SQLAlchemy model
- [x] `user_schemas.py` - Pydantic schemas

### Infrastructure
- [x] `requirements.txt` - All dependencies
- [x] `.env.example` - Template
- [x] `docker-compose.yml` - PostgreSQL 15 + Qdrant
- [x] `Dockerfile` - Multi-stage build

### Migrations
- [x] `alembic.ini` - Config
- [x] `alembic/env.py` - Environment setup
- [x] `001_create_users_table.py` - Initial migration

### Startup Tasks (Do These)
```bash
# 1. Virtual environment
python3.10 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy .env
cp .env.example .env

# 4. Start PostgreSQL
docker-compose up -d

# 5. Wait for PostgreSQL to be ready
docker-compose logs postgres  # Watch for "database system is ready"

# 6. Run migrations
alembic upgrade head

# 7. Verify tables
# psql -U knowledge_user -d knowledge_assistant -c "\dt"
```

---

## Day 3: Auth Endpoints (3 hours)

### Implemented Endpoints
- [x] `POST /auth/signup` - Register new user
  - Input: email, password
  - Output: access_token, user_id
  - Validation: email unique, password hashed
  
- [x] `POST /auth/login` - Login user
  - Input: email, password
  - Output: access_token, user_id
  - Validation: credentials verified
  
- [x] `GET /auth/me` - Get current user (protected)
  - Input: Authorization header (Bearer token)
  - Output: user object (id, email, role, created_at)
  - Validation: token valid and not expired

### Testing Tasks (Do These)
```bash
# Open new terminal, server running on 8000

# Test 1: Health check
curl http://localhost:8000/health

# Test 2: Signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user1@example.com",
    "password": "password123"
  }'
# Copy access_token from response

# Test 3: Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user1@example.com",
    "password": "password123"
  }'

# Test 4: Get current user (replace TOKEN)
TOKEN="your_token_here"
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Test 5: Invalid token (should fail)
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer invalid_token"

# Test 6: Duplicate email (should fail)
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user1@example.com",
    "password": "password123"
  }'
```

### Verification
- [ ] All endpoints return correct status codes (200, 400, 401)
- [ ] Tokens are valid JWT
- [ ] Passwords are hashed in database
- [ ] No plaintext passwords anywhere
- [ ] Endpoints documented in Swagger (/docs)

---

## Day 4: Deploy to Railway (2 hours)

### Setup
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Create project
railway init
```

### Add Database
- [ ] In Railway dashboard, add PostgreSQL service
- [ ] Copy DATABASE_URL from PostgreSQL environment variables

### Set Environment Variables
```bash
railway variable set DATABASE_URL="postgresql://user:pass@host:5432/db"
railway variable set JWT_SECRET="production-secret-key-change-this"
railway variable set JWT_ALGORITHM="HS256"
railway variable set JWT_EXPIRE_MINUTES="30"
railway variable set DEBUG="False"
```

### Deploy
```bash
# Deploy
railway up

# View logs
railway logs -f

# Get public URL
railway logs
```

### Test Deployment
- [ ] Health check works: `https://your-railway-url/health`
- [ ] Signup works
- [ ] Login works
- [ ] Get /me works with token

### URL to Save
```
Backend: https://your-railway-url
```

---

## Documentation & Testing

### Files Created
- [x] `README.md` - Complete setup guide
- [x] `test_auth.py` - Automated test script
- [x] `postman_collection.json` - Postman tests
- [x] `.gitignore` - Don't commit secrets
- [x] `WEEK1_CHECKLIST.md` - This file

### Run Tests Locally
```bash
# Python test script
python test_auth.py

# Should output:
# Testing: Health Check
# ✓ Status: 200
# Testing: Signup (testuser@example.com)
# ✓ Status: 200
# ...
# Results: 7/7 tests passed
```

### Import into Postman
- [ ] Open Postman
- [ ] File → Import → Select `postman_collection.json`
- [ ] Set `base_url` variable to `http://localhost:8000`
- [ ] Run all requests
- [ ] Should see green checkmarks

---

## Final Checklist

### Code Quality
- [ ] No hardcoded secrets in code
- [ ] All imports used
- [ ] Type hints on functions
- [ ] Docstrings on endpoints
- [ ] Error handling on all endpoints

### Security
- [ ] Passwords hashed with bcrypt
- [ ] JWT secret not in repo (in .env)
- [ ] Database credentials not in code
- [ ] No debug=True in production
- [ ] CORS properly configured (localhost for dev)

### Database
- [ ] PostgreSQL running in Docker
- [ ] Alembic migrations applied
- [ ] Users table created
- [ ] Email column has unique index
- [ ] No hardcoded database URLs

### Deployment
- [ ] Railway project created
- [ ] Environment variables set
- [ ] Migrations run automatically on deploy
- [ ] Health check passes on Railway
- [ ] Auth endpoints work on Railway

---

## Common Issues & Fixes

### "connection refused" on PostgreSQL
```bash
docker-compose ps
# If postgres not running:
docker-compose up -d postgres
# Wait 10 seconds
sleep 10
alembic upgrade head
```

### "DATABASE_URL not set"
```bash
# Check .env exists
cat .env

# If missing:
cp .env.example .env
# Edit .env with your values
```

### JWT Secret not working
```bash
# Make sure same secret in .env and what's being used
# Check in config.py it's loaded correctly
python -c "from config import settings; print(settings.jwt_secret)"
```

### Alembic migration failed
```bash
# Check if Alembic dir exists
ls alembic/

# If not:
alembic init alembic

# Then create migration manually
```

### Duplicate Email Not Rejected
```bash
# Check unique constraint on users table
# psql -U knowledge_user -d knowledge_assistant
# \d users
# Should show: "email" UNIQUE
```

---

## Week 1 Done When

- [x] All 7 endpoints implemented
- [x] All endpoints tested (locally + Postman + Python script)
- [x] Deployed to Railway
- [x] Database migrations automatic
- [x] README complete
- [x] No secrets in repo
- [x] Token-based auth working

**Ready for Week 2: RAG Core**

---

## Success Criteria

```
Week 1 Complete = 
  ✓ FastAPI running locally with auth
  ✓ PostgreSQL has users table
  ✓ JWT tokens generated and validated
  ✓ All endpoints return correct status codes
  ✓ Deployed to Railway (health check works)
  ✓ Local docker-compose.yml fully functional
  ✓ Zero secrets in git repo
```

**Start: Monday**
**Done: Friday**
**Next: Week 2 RAG integration**
