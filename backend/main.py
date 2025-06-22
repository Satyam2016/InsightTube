from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from core.config import settings
from core.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="InsightTube API",
    description="YouTube Video Analysis API with AI-powered insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "InsightTube API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)