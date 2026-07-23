from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.lecture_router import router as lecture_router
from database.database import initialize_database
from progress import get_progress

from routers.upload_router import router as upload_router
from routers.ask_router import router as ask_router

# Initialize Database
initialize_database()

# Create FastAPI App
app = FastAPI()

# Register Routers
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(lecture_router)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to LectureMind AI Backend"
    }


@app.get("/status")
def status():
    return get_progress()