# API Reference - Week 1 Endpoints

All endpoints with curl examples and expected responses.

---

## Base URL

**Local:** `http://localhost:8000`
**Production:** `https://your-railway-url`

---

## 1. Health Check

### Request

```bash
curl -X GET http://localhost:8000/health
```

### Response

```
Status: 200 OK

{
  "status": "ok"
}
```

---

## 2. Signup

### Request

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

### Parameters

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | string | Yes | Must be valid email, must be unique |
| password | string | Yes | Will be hashed with bcrypt |

### Response (Success)

```
Status: 200 OK

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}
```

### Response (Error)

```
Status: 400 Bad Request

{
  "detail": "Email already registered"
}
```

### Example Flow

```bash
# Signup
RESPONSE=$(curl -s -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "password123"
  }')

echo $RESPONSE
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "user_id": 1
# }

# Extract token (using jq)
TOKEN=$(echo $RESPONSE | jq -r '.access_token')
echo $TOKEN
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Now use TOKEN in protected requests
```

---

## 3. Login

### Request

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

### Parameters

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | string | Yes | User's registered email |
| password | string | Yes | Plain text password (not hashed) |

### Response (Success)

```
Status: 200 OK

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}
```

### Response (Error - Invalid Credentials)

```
Status: 401 Unauthorized

{
  "detail": "Invalid email or password"
}
```

### Example Flow

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "password123"
  }'

# Response: { access_token, ... }

# Wrong password
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "wrong_password"
  }'

# Response: 401 Unauthorized
```

---

## 4. Get Current User (Protected)

### Request

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Headers

| Header | Value | Required |
|--------|-------|----------|
| Authorization | Bearer {access_token} | Yes |

### Response (Success)

```
Status: 200 OK

{
  "id": 1,
  "email": "user@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00+00:00"
}
```

### Response (Error - Invalid Token)

```
Status: 401 Unauthorized

{
  "detail": "Invalid or expired token"
}
```

### Response (Error - Expired Token)

```
Status: 401 Unauthorized

{
  "detail": "Invalid or expired token"
}
```

### Example Flow

```bash
# Get current user with valid token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Response: { id, email, role, created_at }

# Without token (will fail)
curl -X GET http://localhost:8000/auth/me

# Response: 403 Forbidden (no auth header)

# With invalid token (will fail)
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer invalid_token"

# Response: 401 Unauthorized
```

---

## Common Patterns

### Get Token and Use It

```bash
#!/bin/bash

# Signup and save token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"

# Use token in protected request
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Bash Script for Testing

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "1. Health Check"
curl $BASE_URL/health
echo ""

echo "2. Signup"
RESPONSE=$(curl -s -X POST $BASE_URL/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "testpass123"
  }')
echo $RESPONSE
TOKEN=$(echo $RESPONSE | jq -r '.access_token')

echo ""
echo "3. Login"
curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "testpass123"
  }'
echo ""

echo "4. Get Current User"
curl -s -X GET $BASE_URL/auth/me \
  -H "Authorization: Bearer $TOKEN"
echo ""
```

---

## Token Format

### Headers

```
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

```
{
  "sub": "1",                    // User ID as string
  "email": "user@example.com",
  "exp": 1705315200,            // Expiry (seconds since epoch)
  "iat": 1705313400             // Issued at (seconds since epoch)
}
```

### Signature

```
HMACSHA256(
  base64(header) + "." + base64(payload),
  JWT_SECRET
)
```

---

## Errors

### 400 Bad Request

```json
{
  "detail": "Email already registered"
}
```

Reasons:
- Email not unique during signup
- Invalid email format
- Missing required fields

### 401 Unauthorized

```json
{
  "detail": "Invalid email or password"
}
```

Reasons:
- Wrong password
- Invalid token
- Expired token
- No authorization header

### 404 Not Found

```json
{
  "detail": "User not found"
}
```

Reasons:
- User was deleted
- Token contains invalid user_id

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

Reasons:
- Database connection failed
- Server error (check logs)

---

## Testing Tools

### cURL (Command Line)

```bash
# Simple GET
curl http://localhost:8000/health

# POST with JSON
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass"}'

# With Authorization header
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer TOKEN_HERE"

# Pretty print (requires jq)
curl -s http://localhost:8000/health | jq
```

### HTTPie (Better cURL)

```bash
# Install
pip install httpie

# GET
http localhost:8000/health

# POST
http POST localhost:8000/auth/signup \
  email=user@example.com \
  password=password123

# With header
http GET localhost:8000/auth/me \
  "Authorization: Bearer TOKEN"
```

### Postman

Import `postman_collection.json`:
1. Open Postman
2. File → Import
3. Select `postman_collection.json`
4. Set `base_url` variable
5. Run requests

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Signup
response = requests.post(
    f"{BASE_URL}/auth/signup",
    json={"email": "user@example.com", "password": "password123"}
)
token = response.json()["access_token"]

# Get current user
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
user = response.json()
print(user)
```

---

## Rate Limiting

Not implemented in Week 1. Add in Week 4 (production hardening).

---

## CORS

Currently allows all origins (`*`). Change in production:

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

**API Reference Complete**

See `ARCHITECTURE.md` for flow diagrams.
