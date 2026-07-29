from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.exceptions import register_exception_handlers
from core.logging import configure_logging
from routers.lecture_router import router as lecture_router
from routers.auth_router import router as auth_router
from progress import get_progress
from routers.summary_router import router as summary_router
from routers.keypoints_router import router as keypoints_router
from routers.upload_router import router as upload_router
from routers.ask_router import router as ask_router
from routers.notes_router import router as notes_router
from routers.quiz_router import router as quiz_router
from utils.responses import success_response

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

register_exception_handlers(app)

from database.database import initialize_database

initialize_database()

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(lecture_router)
app.include_router(summary_router)
app.include_router(notes_router)
app.include_router(keypoints_router)
app.include_router(quiz_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return success_response(
        "Welcome to LectureMind AI Backend",
        legacy={"message": "Welcome to LectureMind AI Backend"},
    )


@app.get("/status")
def status():
    progress = get_progress()
    return success_response(
        "Progress fetched successfully.",
        data=progress,
        legacy=progress,
    )
