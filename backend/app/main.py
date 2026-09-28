from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Problem, TestCase, Submission
from app.api import problems, submissions

# Creates all tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexusCP API")

# Allows React (localhost:5173) to talk to FastAPI (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems.router)
app.include_router(submissions.router)

@app.get("/")
def root():
    return {"status": "NexusCP API running"}