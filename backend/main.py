
from fastapi import FastAPI
from routers import analyze

app = FastAPI(
    title="YouTube Video Analyzer",
    description="Analyze YouTube videos using AI for comments, content, and recommendations",
    version="1.0.0"
)

app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "YouTube Analyzer Backend is running."}
