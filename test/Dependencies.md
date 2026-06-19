# Dependencies Explained

All packages used in the project and why.

## Core Framework

**fastapi (0.104.1)**
- Modern async Python web framework
- Auto-generates OpenAPI/Swagger docs
- Type-safe with Pydantic validation
- Industry standard for APIs
- Why: Production-grade, fast, well-documented

**uvicorn (0.24.0)**
- ASGI server for FastAPI
- High-performance async HTTP server
- Production-ready with good logging
- Why: Runs FastAPI, lightweight

## Database

**sqlalchemy (2.0.23)**
- Python ORM for database abstraction
- Supports PostgreSQL, MySQL, SQLite, etc.
- Prevents SQL injection automatically
- Query builder and relationship management
- Why: Industry standard, safe, flexible

**psycopg2-binary (2.9.9)**
- PostgreSQL adapter for Python
- Native PostgreSQL driver
- Binary build (no compilation needed)
- Why: Connects SQLAlchemy to PostgreSQL

**alembic (1.13.0)**
- Database migration tool for SQLAlchemy
- Version control for database schema
- Auto-generates migrations from models
- Supports up/down migrations
- Why: Track schema changes, deploy safely

## Data Validation

**pydantic (2.5.0)**
- Data validation using Python type hints
- Auto-generates JSON schemas
- Converts input to Python types
- Runtime validation with error messages
- Why: Request/response validation, security

**pydantic-settings (2.1.0)**
- Load environment variables into Pydantic models
- Validation of configuration
- Type checking for settings
- Why: Safe, typed configuration management

## Authentication & Security

**python-jose[cryptography] (3.3.0)**
- JWT (JSON Web Token) implementation
- Token encoding/decoding and validation
- Supports HS256 algorithm
- Why: Industry standard for API authentication

**bcrypt (4.1.1)**
- Password hashing algorithm
- Deliberately slow (resists brute force)
- Automatic salt generation per password
- Industry standard for password storage
- Why: Secure password hashing

## Utilities

**python-multipart (0.0.6)**
- Parse multipart form data
- Needed for file uploads
- Works with FastAPI's UploadFile
- Why: Required for future file upload endpoint

**python-dotenv (1.0.0)**
- Load environment variables from .env files
- Doesn't override existing env vars
- Safe for development
- Why: Local development configuration

## Testing & Development (Optional)

**pytest (7.4.3)**
- Python testing framework
- Unit and integration tests
- Fixtures for setup/teardown
- Why: Standard Python test runner

**pytest-asyncio (0.21.1)**
- Async test support for pytest
- Tests async functions (FastAPI endpoints)
- Why: Test async code properly

**httpx (0.25.0)**
- Async HTTP client for testing
- FastAPI's test client uses it
- Why: Test API endpoints

## Why These Specific Versions?

We use **exact versions** (e.g., `fastapi==0.104.1`) not ranges (e.g., `fastapi>=0.100.0`) because:

1. **Reproducibility** — Same code, same dependencies
2. **Production safety** — No unexpected breaking changes
3. **Testing** — Tests validated against exact versions
4. **Consistency** — Dev, test, and production identical

## Total Size

```
pip install -r requirements.txt
→ ~200MB with all dependencies
→ ~150MB for just core packages
```

## Future Dependencies (Week 2+)

Once you move to Week 2, you'll add:

**For PDF/DOCX extraction:**
- `pdfplumber` — PDF text extraction
- `python-docx` — Word document parsing

**For embeddings:**
- `openai` — OpenAI API for embeddings
- `google-generativeai` — Gemini API

**For vector search:**
- `qdrant-client` — Qdrant vector database client

**For LLM integration:**
- `langchain` — LLM chains and agents
- `langchain-openai` — LangChain + OpenAI

**For text processing:**
- `nltk` — Text tokenization and processing

## Security Notes

- ✅ No insecure packages
- ✅ No packages with known vulnerabilities (as of Jan 2024)
- ✅ All packages are actively maintained
- ✅ Major packages used in production systems

## Performance

Current dependencies are lightweight:

```
fastapi         ~1MB
sqlalchemy      ~2MB
pydantic        ~1MB
alembic         ~0.5MB
bcrypt          ~0.3MB
```

Total: ~5MB core dependencies (very small)

## Updating Dependencies

To update safely:

```bash
# Check for updates
pip list --outdated

# Update one package
pip install --upgrade fastapi

# Update and pin to requirements.txt
pip freeze > requirements.txt
```

Always test after updating!

## License Check

All packages use permissive licenses:
- FastAPI → MIT
- SQLAlchemy → MIT
- Pydantic → MIT
- Alembic → MIT
- Bcrypt → Apache 2.0
- Python-jose → MIT
- Uvicorn → BSD

Safe for commercial use. ✓
