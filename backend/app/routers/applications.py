from fastapi import APIRouter, HTTPException

from ..database import db_cursor
from ..schemas import ApplicationCreate, StatusUpdate

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.get("")
def list_applications(student_id: int | None = None):
    query = """
        SELECT
            a.id,
            a.student_id,
            a.job_id,
            s.name AS student,
            j.title AS job,
            c.name AS company,
            j.location,
            a.status,
            a.applied_at
        FROM applications a
        JOIN students s ON s.id = a.student_id
        JOIN jobs j ON j.id = a.job_id
        JOIN companies c ON c.id = j.company_id
    """
    params = []
    if student_id:
        query += " WHERE a.student_id = %s"
        params.append(student_id)
    query += " ORDER BY a.id DESC"

    with db_cursor() as (_, cursor):
        cursor.execute(query, params)
        return cursor.fetchall()


@router.post("", status_code=201)
def create_application(application: ApplicationCreate):
    with db_cursor() as (connection, cursor):
        cursor.execute("SELECT id FROM students WHERE id = %s", (application.student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")

        cursor.execute("SELECT id FROM jobs WHERE id = %s", (application.job_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job not found")

        cursor.execute("""
            SELECT id FROM applications
            WHERE student_id = %s AND job_id = %s
        """, (application.student_id, application.job_id))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Student has already applied for this job")

        cursor.execute("""
            INSERT INTO applications (student_id, job_id, status)
            VALUES (%s, %s, 'Applied')
        """, (application.student_id, application.job_id))
        connection.commit()
        return {"message": "Application submitted successfully", "application_id": cursor.lastrowid}


@router.patch("/{application_id}/status")
def update_application_status(application_id: int, payload: StatusUpdate):
    with db_cursor() as (connection, cursor):
        cursor.execute("SELECT id FROM applications WHERE id = %s", (application_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")

        cursor.execute(
            "UPDATE applications SET status = %s WHERE id = %s",
            (payload.status, application_id),
        )
        connection.commit()
        return {"message": "Application status updated", "status": payload.status}
