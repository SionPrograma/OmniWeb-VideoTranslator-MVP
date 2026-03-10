from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import process, health
from .config import settings
import uvicorn

app = FastAPI(
    title=settings.APP_NAME,
    description="Professional Video Translator MVP - Part of OmniWeb Ecosystem",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (Frontend and Outputs)
app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="outputs")

# Include Routers
app.include_router(process.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
