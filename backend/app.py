"""FastAPI main application for Pupil Development Tracker."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal
from models import Category
from routes import school_years, classes, pupils, categories, entries
from routes import reports, export

app = FastAPI(
    title="Pupil Development Tracker",
    description="API for tracking pupil development",
    version="1.0.0",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(school_years.router, prefix="/school_years", tags=["School Years"])
app.include_router(classes.router, prefix="/classes", tags=["Classes"])
app.include_router(pupils.router, prefix="/pupils", tags=["Pupils"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(entries.router, prefix="/entries", tags=["Entries"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(export.router, tags=["Export/Import"])


PREDEFINED_CATEGORIES = [
    ("Arbeitsverhalten", "Work Behavior"),
    ("Sozialverhalten", "Social Behavior"),
    ("Lernentwicklung", "Learning Development"),
    ("Besondere Vorkommnisse", "Special Incidents"),
    ("Motorik", "Motor Skills"),
    ("Kreativitaet", "Creativity"),
    ("Sprachentwicklung", "Language Development"),
    ("Selbststaendigkeit", "Independence"),
]


def seed_categories():
    """Seed predefined categories if they don't exist."""
    db = SessionLocal()
    try:
        existing = db.query(Category).filter(Category.is_predefined == True).count()
        if existing == 0:
            for name_de, name_en in PREDEFINED_CATEGORIES:
                cat = Category(name_de=name_de, name_en=name_en, is_predefined=True)
                db.add(cat)
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    seed_categories()


@app.get("/")
async def root():
    """Root endpoint returning API info."""
    return {"message": "Pupil Development Tracker API", "version": "1.0.0"}
