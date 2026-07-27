from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.lecture_router import router as lecture_router
from progress import get_progress
from routers.summary_router import router as summary_router
from routers.keypoints_router import router as keypoints_router
from routers.upload_router import router as upload_router
from routers.ask_router import router as ask_router
from routers.notes_router import router as notes_router
from routers.quiz_router import router as quiz_router
# Initialize Database

# Create FastAPI App
app = FastAPI()

# Register Routers
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(lecture_router)
app.include_router(summary_router)
app.include_router(notes_router)
app.include_router(keypoints_router)
app.include_router(quiz_router)
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