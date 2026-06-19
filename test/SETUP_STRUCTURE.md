# Directory Structure Setup

Copy these files to the correct locations in your backend/ directory.

## File Organization

```
backend/
│
├── 📄 Main Python Files (copy to root)
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── security.py
│   ├── jwt_utils.py
│   └── auth.py
│
├── 📁 app/ (create directory)
│   ├── __init__.py (empty file)
│   │
│   ├── 📁 api/
│   │   ├── __init__.py (empty file)
│   │   └── auth.py (symlink or copy auth.py here)
│   │
│   ├── 📁 core/
│   │   ├── __init__.py (empty file)
│   │   ├── config.py (copy here)
│   │   ├── security.py (copy here)
│   │   └── jwt_utils.py (copy here)
│   │
│   ├── 📁 models/
│   │   ├── __init__.py (empty file)
│   │   └── users.py
│   │
│   ├── 📁 schemas/
│   │   ├── __init__.py (empty file)
│   │   └── users.py (copy user_schemas.py here)
│   │
│   └── db.py (copy here)
│
├── 📁 alembic/ (Alembic will auto-create this)
│   ├── __init__.py (empty)
│   ├── env.py (copy alembic_env.py here)
│   ├── script.py.mako (copy alembic_script.py.mako here)
│   │
│   └── 📁 versions/
│       ├── __init__.py (empty)
│       └── 001_create_users_table.py
│
├── 📄 Configuration Files (copy to root)
│   ├── requirements.txt
│   ├── .env (copy .env.example to .env, update values)
│   ├── .env.example
│   ├── .gitignore
│   ├── .dockerignore
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── Makefile
│
├── 📁 tests/ (create directory)
│   ├── __init__.py (empty)
│   └── test_auth.py (copy here)
│
├── 📁 docs/ (create directory for documentation)
│   ├── 00_START_HERE.md
│   ├── INDEX.md
│   ├── QUICK_START.md
│   ├── README.md
│   ├── WEEK1_CHECKLIST.md
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── RAILWAY_DEPLOY.md
│   ├── DELIVERY_SUMMARY.md
│   └── FILE_MANIFEST.txt
│
├── 📁 postman/ (create directory)
│   └── postman_collection.json
│
└── venv/ (created by: python3.10 -m venv venv)
```

## Setup Instructions

### Step 1: Create Directory Structure

```bash
cd backend

# Create directories
mkdir -p app/api app/core app/models app/schemas
mkdir -p alembic/versions
mkdir -p tests
mkdir -p docs
mkdir -p postman
```

### Step 2: Copy Files to Root

```bash
# Configuration files
cp .env.example .env
cp .gitignore .gitignore
cp .dockerignore .dockerignore
cp docker-compose.yml docker-compose.yml
cp Dockerfile Dockerfile
cp alembic.ini alembic.ini
cp pyproject.toml pyproject.toml
cp Makefile Makefile
cp requirements.txt requirements.txt

# Main files to root
cp main.py main.py
cp config.py config.py
cp db.py db.py
cp security.py security.py
cp jwt_utils.py jwt_utils.py
cp auth.py auth.py
```

### Step 3: Copy Files to app/

```bash
# app/__init__.py (empty)
touch app/__init__.py

# app/api/
touch app/api/__init__.py
cp auth.py app/api/auth.py

# app/core/
touch app/core/__init__.py
cp config.py app/core/config.py
cp security.py app/core/security.py
cp jwt_utils.py app/core/jwt_utils.py

# app/models/
touch app/models/__init__.py
cp users.py app/models/users.py

# app/schemas/
touch app/schemas/__init__.py
cp user_schemas.py app/schemas/users.py

# app/db.py
cp db.py app/db.py
```

### Step 4: Copy Files to alembic/

```bash
# alembic/__init__.py (empty)
touch alembic/__init__.py

# alembic/env.py
cp alembic_env.py alembic/env.py

# alembic/script.py.mako
cp alembic_script.py.mako alembic/script.py.mako

# alembic/versions/
touch alembic/versions/__init__.py
cp 001_create_users_table.py alembic/versions/001_create_users_table.py
```

### Step 5: Copy Documentation

```bash
# docs/
cp 00_START_HERE.md docs/00_START_HERE.md
cp INDEX.md docs/INDEX.md
cp QUICK_START.md docs/QUICK_START.md
cp README.md docs/README.md
cp WEEK1_CHECKLIST.md docs/WEEK1_CHECKLIST.md
cp ARCHITECTURE.md docs/ARCHITECTURE.md
cp API_REFERENCE.md docs/API_REFERENCE.md
cp RAILWAY_DEPLOY.md docs/RAILWAY_DEPLOY.md
cp DELIVERY_SUMMARY.md docs/DELIVERY_SUMMARY.md
cp FILE_MANIFEST.txt docs/FILE_MANIFEST.txt

# postman/
cp postman_collection.json postman/postman_collection.json

# tests/
touch tests/__init__.py
cp test_auth.py tests/test_auth.py
```

### Step 6: Update .env

Edit `.env` with your actual values:

```bash
DATABASE_URL=postgresql://knowledge_user:knowledge_password@localhost:5432/knowledge_assistant
JWT_SECRET=your-super-secret-key-change-in-production-32-chars-minimum
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
DEBUG=True
```

### Step 7: Verify Structure

```bash
tree backend/ -L 3
# or
find backend -type f -name "*.py" | head -20
```

You should see:
```
backend/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── jwt_utils.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── users.py
│   └── db.py
├── alembic/
│   ├── __init__.py
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── __init__.py
│       └── 001_create_users_table.py
├── tests/
│   ├── __init__.py
│   └── test_auth.py
├── docs/
│   ├── 00_START_HERE.md
│   └── ... (other docs)
├── main.py
├── auth.py
├── config.py
├── db.py
├── security.py
├── jwt_utils.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pyproject.toml
└── Makefile
```

### Step 8: Setup Virtual Environment

```bash
cd backend
python3.10 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Step 9: Start Services

```bash
docker-compose up -d
sleep 10
alembic upgrade head
```

### Step 10: Run Server

```bash
python -m uvicorn main:app --reload
# Server at http://localhost:8000
```

## Quick Commands

Once set up, use Makefile:

```bash
make setup      # Create venv
make install    # Install deps
make docker-up  # Start database
make migrate    # Run migrations
make dev        # Run server
make test       # Run tests
make clean      # Clean cache
```

## Notes

- **Optional:** You can keep all Python files in root or organize them in app/ — both work
- **Option 1 (Flat):** Keep main.py, auth.py, config.py, etc. in root → Simpler but less scalable
- **Option 2 (Structured):** Organize into app/api/, app/core/, app/models/, app/schemas/ → Better for Week 2+

For this project, **use Option 2** (structured) since we'll add more modules in Week 2.

## Verification

After setup, verify everything:

```bash
# Check imports
python -c "from app.api import auth; print('✓ Imports work')"

# Check database
alembic current

# Check server
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```

All done! 🚀
