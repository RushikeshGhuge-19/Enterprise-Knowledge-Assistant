from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test.db import engine, Base
import test.auth as auth
import test.users as users  # Import to register models

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="RAG-powered knowledge assistant backend",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Enterprise Knowledge Assistant",
        "version": "0.1.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
