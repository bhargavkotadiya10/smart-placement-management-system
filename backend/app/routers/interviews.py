from fastapi import APIRouter, HTTPException

from ..database import db_cursor
from ..schemas import InterviewCreate

router = APIRouter(prefix="/api/interviews", tags=["Interviews"])


@router.get("")
def list_interviews():
    with db_cursor() as (_, cursor):
        cursor.execute("""
            SELECT
                i.id,
                i.application_id,
                s.name AS student,
                c.name AS company,
                j.title AS job,
                i.round_name,
                i.scheduled_at,
                i.mode,
                i.notes,
                i.created_at
            FROM interviews i
            JOIN applications a ON a.id = i.application_id
            JOIN students s ON s.id = a.student_id
            JOIN jobs j ON j.id = a.job_id
            JOIN companies c ON c.id = j.company_id
            ORDER BY i.scheduled_at
        """)
        return cursor.fetchall()


@router.post("", status_code=201)
def create_interview(interview: InterviewCreate):
    with db_cursor() as (connection, cursor):
        cursor.execute("SELECT id FROM applications WHERE id = %s", (interview.application_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")

        cursor.execute("""
            INSERT INTO interviews (application_id, round_name, scheduled_at, mode, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            interview.application_id,
            interview.round_name.strip(),
            interview.scheduled_at,
            interview.mode.strip(),
            interview.notes,
        ))
        connection.commit()
        return {"message": "Interview scheduled successfully", "interview_id": cursor.lastrowid}
