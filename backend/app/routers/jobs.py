from fastapi import APIRouter, HTTPException, Query

from ..database import db_cursor
from ..schemas import JobCreate

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("")
def list_jobs(search: str | None = Query(default=None), location: str | None = Query(default=None)):
    query = """
        SELECT
            j.id,
            j.company_id,
            c.name AS company,
            j.title,
            j.location,
            j.internship_duration,
            j.stipend,
            j.salary,
            j.description,
            j.skills,
            j.min_percentage,
            j.openings,
            j.created_at
        FROM jobs j
        JOIN companies c ON c.id = j.company_id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (j.title LIKE %s OR c.name LIKE %s OR j.skills LIKE %s)"
        term = f"%{search}%"
        params.extend([term, term, term])

    if location:
        query += " AND j.location LIKE %s"
        params.append(f"%{location}%")

    query += " ORDER BY j.id DESC"

    with db_cursor() as (_, cursor):
        cursor.execute(query, params)
        return cursor.fetchall()


@router.get("/{job_id}")
def get_job(job_id: int):
    with db_cursor() as (_, cursor):
        cursor.execute("""
            SELECT
                j.id, j.company_id, c.name AS company, j.title, j.location,
                j.internship_duration, j.stipend, j.salary, j.description,
                j.skills, j.min_percentage, j.openings, j.created_at
            FROM jobs j
            JOIN companies c ON c.id = j.company_id
            WHERE j.id = %s
        """, (job_id,))
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job


@router.post("", status_code=201)
def create_job(job: JobCreate):
    with db_cursor() as (connection, cursor):
        cursor.execute("SELECT id FROM companies WHERE id = %s", (job.company_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Company not found")

        cursor.execute("""
            INSERT INTO jobs
            (company_id, title, location, internship_duration, stipend, salary,
             description, skills, min_percentage, openings)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            job.company_id,
            job.title.strip(),
            job.location.strip(),
            job.internship_duration,
            job.stipend,
            job.salary,
            job.description,
            job.skills,
            job.min_percentage,
            job.openings,
        ))
        connection.commit()
        return {"message": "Job created successfully", "job_id": cursor.lastrowid}
