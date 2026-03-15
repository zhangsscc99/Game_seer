from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.database import Base, engine
from routers import auth, tasks, elves, boss, profile, achievements

# Import all models so SQLAlchemy can discover them for create_all
import models.user       # noqa: F401
import models.task       # noqa: F401
import models.elf        # noqa: F401
import models.boss       # noqa: F401
import models.achievement  # noqa: F401

app = FastAPI(
    title="Game Seer API",
    description="游戏化计划应用后端 API（类赛尔号题材）",
    version="0.1.0",
)

# CORS configuration – allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with /api/v1 prefix
API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(tasks.router, prefix=API_PREFIX)
app.include_router(elves.router, prefix=API_PREFIX)
app.include_router(boss.router, prefix=API_PREFIX)
app.include_router(profile.router, prefix=API_PREFIX)
app.include_router(achievements.router, prefix=API_PREFIX)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    """Create all database tables on startup."""
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Game Seer API is running", "docs": "/docs"}
