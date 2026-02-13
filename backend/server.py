from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routes import chat, tasks, skills, users, memory, notifications

# Global database client
db_client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global db_client, db
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/moltbot')
    db_client = AsyncIOMotorClient(mongo_url)
    db = db_client.moltbot
    
    # Install default skills on startup
    from services.skill_service import SkillService
    skill_service = SkillService(db)
    await skill_service.install_default_skills()
    
    print("✅ Database connected and initialized")
    yield
    
    # Shutdown
    if db_client:
        db_client.close()
        print("✅ Database connection closed")

# Create FastAPI app
app = FastAPI(
    title="Moltbot API",
    description="AI-powered personal assistant with memory, tasks, and skills",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(tasks.router)
app.include_router(skills.router)
app.include_router(users.router)
app.include_router(memory.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return {
        "message": "Moltbot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    try:
        # Check database connection
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "ai_service": "ready"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
