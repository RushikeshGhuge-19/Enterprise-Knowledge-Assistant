# Architecture - Week 1

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Client (React)                       │
│                                                               │
│  1. Signup/Login Page                                        │
│  2. Store JWT in localStorage                               │
│  3. Send token in Authorization header                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   FastAPI Backend                            │
│                  (Port 8000)                                 │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Auth Endpoints                                          │ │
│  │                                                          │ │
│  │ POST /auth/signup                                      │ │
│  │  ├─ Validate email (unique)                           │ │
│  │  ├─ Hash password (bcrypt, 12 rounds)                │ │
│  │  ├─ Store in database                                │ │
│  │  └─ Return JWT token                                 │ │
│  │                                                          │ │
│  │ POST /auth/login                                      │ │
│  │  ├─ Find user by email                               │ │
│  │  ├─ Verify password hash                             │ │
│  │  └─ Return JWT token                                 │ │
│  │                                                          │ │
│  │ GET /auth/me (Protected)                             │ │
│  │  ├─ Extract token from Authorization header         │ │
│  │  ├─ Verify JWT signature & expiry                   │ │
│  │  └─ Return user object                              │ │
│  │                                                          │ │
│  │ GET /health                                           │ │
│  │  └─ Return {"status": "ok"}                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQL
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               PostgreSQL Database                            │
│               (Port 5432)                                    │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ users table                                             │ │
│  │                                                          │ │
│  │  Column          │  Type      │  Constraint           │ │
│  │  ──────────────────────────────────────────────────   │ │
│  │  id              │  INTEGER   │  PRIMARY KEY          │ │
│  │  email           │  VARCHAR   │  UNIQUE, NOT NULL    │ │
│  │  password_hash   │  VARCHAR   │  NOT NULL            │ │
│  │  role            │  ENUM      │  DEFAULT 'user'      │ │
│  │  created_at      │  TIMESTAMP │  NOT NULL            │ │
│  │                                                          │ │
│  │  Example row:                                          │ │
│  │  1 │ user@example.com │ $2b$12$... │ user │ 2024-01-15 │ │
│  │                                                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

### Signup

```
Client                          FastAPI                 Database
  │                               │                         │
  │─── POST /auth/signup ────────>│                         │
  │     { email, password }       │                         │
  │                               │─ Hash password (bcrypt)─│
  │                               │  bcrypt.hashpw()       │
  │                               │                         │
  │                               │─ Check email exists ───>│
  │                               │  SELECT * FROM users    │
  │                               │<─────────────────────────│
  │                               │  (not found)            │
  │                               │                         │
  │                               │─ Insert user ─────────>│
  │                               │  INSERT INTO users(...) │
  │                               │<─────────────────────────│
  │                               │  (success, id=1)        │
  │                               │                         │
  │                               │─ Generate JWT ─────────│
  │                               │  jwt.encode()          │
  │<──── 200 OK ────────────────────                        │
  │     { access_token, user_id }                           │
  │                               │                         │
  │─ Store token in localStorage ─>                         │
  │                               │                         │
```

### Login

```
Client                          FastAPI                 Database
  │                               │                         │
  │─── POST /auth/login ─────────>│                         │
  │     { email, password }       │                         │
  │                               │─ Find user ───────────>│
  │                               │  SELECT * FROM users    │
  │                               │  WHERE email = ...      │
  │                               │<─────────────────────────│
  │                               │  (found)                │
  │                               │                         │
  │                               │─ Verify password ──────│
  │                               │  bcrypt.checkpw()      │
  │                               │  (matches)             │
  │                               │                         │
  │                               │─ Generate JWT ─────────│
  │                               │  jwt.encode()          │
  │<──── 200 OK ────────────────────                        │
  │     { access_token, user_id }                           │
  │                               │                         │
```

### Protected Request (Get Current User)

```
Client                          FastAPI                 Database
  │                               │                         │
  │─── GET /auth/me ────────────>│                         │
  │     Authorization: Bearer ... │                         │
  │                               │─ Extract token ────────│
  │                               │  credentials.credentials
  │                               │                         │
  │                               │─ Verify JWT ──────────│
  │                               │  jwt.decode()         │
  │                               │  (valid & not expired) │
  │                               │                         │
  │                               │─ Get user_id from JWT ─│
  │                               │  payload.get("sub")   │
  │                               │                         │
  │                               │─ Query user ──────────>│
  │                               │  SELECT * FROM users    │
  │                               │  WHERE id = 1          │
  │                               │<─────────────────────────│
  │                               │  (user object)         │
  │<──── 200 OK ────────────────────                        │
  │     { id, email, role, ... }                            │
  │                               │                         │
```

---

## JWT Token Structure

### What's Inside?

```json
{
  "sub": "1",           // User ID
  "email": "user@example.com",
  "exp": 1705315200,    // Expiry timestamp (30 min from now)
  "iat": 1705313400     // Issued at timestamp
}
```

### Encoded Token

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwi
ZXhwIjoxNzA1MzE1MjAwLCJpYXQiOjE3MDUzMTM0MDB9.
FjU4rYHlLYFYE_F8f-w8LDjX9ZxKJcZBnDh3vHs7QXY
```

**Format:** `header.payload.signature`

- **Header**: Algorithm (HS256) + type (JWT)
- **Payload**: Claims (sub, email, exp, iat)
- **Signature**: HMAC-SHA256(header + payload, JWT_SECRET)

---

## Password Security

### Why Bcrypt?

```
Plain Password:     "secure_password_123"
                            ↓
                    bcrypt.hashpw()
                    (12 rounds = slow)
                            ↓
Hashed:             "$2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcg7b3XeKeUxWdeS86AGR..."
                            ↓
                    Never stored as plaintext
                    Each password has unique salt
                    Takes ~0.3 seconds to hash
```

### During Login

```
User enters password: "secure_password_123"
                            ↓
bcrypt.checkpw(password, stored_hash)
                            ↓
Compares hashes (NOT original passwords)
                            ↓
Returns True/False
```

**Key Benefits:**
- Even if database is stolen, passwords are safe
- Bcrypt is deliberately slow (resists brute force)
- If computers get faster, increase rounds
- Each password has unique salt (no rainbow tables)

---

## Error Handling

### Status Codes

```
200 OK
    ✓ Request successful
    ✓ Used for: login, signup, get user

400 Bad Request
    ✗ Email already exists during signup
    ✗ Invalid email format
    ✗ Missing required fields

401 Unauthorized
    ✗ Invalid or expired token
    ✗ Wrong password
    ✗ No Authorization header

500 Internal Server Error
    ✗ Database connection failed
    ✗ Unexpected error (check logs)
```

---

## Deployment Architecture

### Local Development

```
Your Machine
├── Python app (port 8000)
├── PostgreSQL (port 5432, Docker)
└── Browser (http://localhost:8000/docs)
```

### Production (Railway)

```
Railway Cloud
├── FastAPI container (auto-scaled)
├── PostgreSQL service (managed)
└── HTTPS (provided by Railway)

Client → HTTPS → Railway → PostgreSQL
```

---

## Data Flow Summary

```
1. User submits email + password
2. Backend hashes password with bcrypt (12 rounds)
3. Stores user in PostgreSQL (email unique)
4. Generates JWT token with user_id
5. Returns token to client
6. Client stores in localStorage
7. Client sends token in Authorization header
8. Backend verifies JWT signature
9. Backend queries user by ID from token
10. Returns user object
```

---

## Next: Week 2

Once auth is working:

```
Week 1 (Done)
├── Users table
├── Password hashing
├── JWT generation
└── Protected endpoints

Week 2 (Next)
├── Documents table (file uploads)
├── Chunk storage (text pieces)
├── Embeddings service (OpenAI/Gemini)
├── Qdrant integration (vector search)
└── RAG chat endpoint
```

---

**Architecture complete. Ready to build Week 2!**
