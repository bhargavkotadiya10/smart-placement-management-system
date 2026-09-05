from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import db_cursor
from .routers import applications, companies, interviews, jobs, students

app = FastAPI(
    title="Smart Placement Management System",
    description="Placement management REST API for students, companies, jobs, applications and interviews.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(students.router)
app.include_router(applications.router)
app.include_router(interviews.router)


@app.get("/api/health", tags=["System"])
def health_check():
    try:
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT 1 AS ok")
            cursor.fetchone()
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "ok", "database": "unavailable"}


@app.get("/api/dashboard", tags=["Dashboard"])
def dashboard():
    with db_cursor() as (_, cursor):
        cursor.execute("SELECT COUNT(*) AS total FROM students")
        students_count = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM companies")
        companies_count = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM jobs")
        jobs_count = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM applications")
        applications_count = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM applications WHERE status = 'Selected'")
        selected_count = cursor.fetchone()["total"]

    return {
        "students": students_count,
        "companies": companies_count,
        "jobs": jobs_count,
        "applications": applications_count,
        "selected": selected_count,
    }


@app.get("/", include_in_schema=False)
def home():
    return {"message": "Smart Placement Management System API is running"}


frontend_path = Path(__file__).resolve().parents[2] / "frontend"
if frontend_path.exists():
    app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")
