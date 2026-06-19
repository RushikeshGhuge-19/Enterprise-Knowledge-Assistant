# Deploy to Railway

Complete production deployment guide.

---

## Prerequisites

- Railway account (free) → https://railway.app
- GitHub account (to connect repo)
- Code pushed to GitHub

---

## Step 1: Create Railway Project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login
# Opens browser, authenticate

# Create new project (in your backend directory)
railway init
```

---

## Step 2: Add PostgreSQL Database

In Railway dashboard:

1. Click **New** → **Database** → **PostgreSQL**
2. Wait for it to spin up (1-2 min)
3. Copy the `DATABASE_URL` from PostgreSQL service variables
4. Save it somewhere (you'll need it next)

---

## Step 3: Configure Environment Variables

```bash
# Set all variables
railway variable set DATABASE_URL="postgresql://..."
railway variable set JWT_SECRET="your-super-secret-production-key"
railway variable set JWT_ALGORITHM="HS256"
railway variable set JWT_EXPIRE_MINUTES="30"
railway variable set DEBUG="False"
```

Verify they're set:
```bash
railway variable list
```

---

## Step 4: Deploy

```bash
# Deploy from current directory
railway up
```

The CLI will:
1. Build Docker image
2. Push to Railway registry
3. Start container
4. Run migrations (if alembic/ exists)

---

## Step 5: Get Your URL

```bash
# View logs and find the public URL
railway logs

# Or check dashboard:
# Services → Backend → Domains → copy the URL
```

Save your URL:
```
https://your-project-name.up.railway.app
```

---

## Step 6: Test Deployment

```bash
BASE_URL="https://your-project-name.up.railway.app"

# Health check
curl $BASE_URL/health

# Signup
curl -X POST $BASE_URL/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# If you get a 200 response with a token → **You're live!**
```

---

## Step 7: Connect to Frontend

Update your frontend `.env`:

```
REACT_APP_API_URL=https://your-project-name.up.railway.app
```

---

## Monitoring

### View Logs
```bash
railway logs -f
```

### View Metrics
```bash
railway status
```

### Restart Service
```bash
railway restart
```

---

## Auto-Deploy (Optional)

Connect GitHub repo for auto-deploy on push:

1. Railway Dashboard → Deployments
2. Click **Connect Repository**
3. Select your GitHub repo
4. Enable "Auto-deploy on push"

Now every `git push` automatically deploys.

---

## Troubleshooting

### Build Failed
```bash
railway logs -f
# Check error message, usually:
# - Python version mismatch
# - Missing requirements.txt
# - Invalid Dockerfile
```

### Health Check Fails
```bash
# Make sure GET /health endpoint exists
# Check if database connection failed in logs
railway logs -f | grep ERROR
```

### Database Connection Refused
```bash
# Make sure DATABASE_URL is set correctly
railway variable list | grep DATABASE

# Check format:
# postgresql://user:pass@host:5432/db
```

### Migrations Didn't Run
```bash
# Manually run migrations
railway run alembic upgrade head

# Or check if alembic.ini exists in repo
ls alembic/
```

---

## Production Checklist

- [ ] JWT_SECRET is strong (32+ chars, random)
- [ ] DEBUG=False in production
- [ ] DATABASE_URL doesn't have localhost
- [ ] CORS origins set to frontend URL (not *)
- [ ] Health endpoint returns 200
- [ ] Auth endpoints tested with real token
- [ ] Logs show no errors on deploy
- [ ] Database connection stable
- [ ] Migrations applied automatically

---

## Scaling

As you grow Week 2-4:

1. **Add more env vars** (OpenAI API key, etc.)
   ```bash
   railway variable set OPENAI_API_KEY="sk-..."
   ```

2. **Monitor database size**
   - PostgreSQL has generous free tier
   - Can upgrade in Railway dashboard

3. **Watch logs for errors**
   ```bash
   railway logs -f | grep ERROR
   ```

---

## Cost

Railway free tier covers:
- 1 PostgreSQL database ✓
- 1 Backend service ✓
- ~500 hours/month runtime ✓

**No credit card required for free tier.**

---

## Need Help?

- Railway docs: https://railway.app/docs
- GitHub issues with logs
- Check `railway logs -f` for errors

---

**Your backend is now live and deployed! 🚀**

Next: Deploy frontend to Vercel (Week 3)
