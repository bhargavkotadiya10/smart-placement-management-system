from fastapi import APIRouter, HTTPException

from ..database import db_cursor
from ..schemas import StudentCreate

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("")
def list_students():
    with db_cursor() as (_, cursor):
        cursor.execute("""
            SELECT id, name, email, phone, course, graduation_year,
                   percentage, github_url, linkedin_url, created_at
            FROM students
            ORDER BY id DESC
        """)
        return cursor.fetchall()


@router.get("/{student_id}")
def get_student(student_id: int):
    with db_cursor() as (_, cursor):
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student


@router.post("", status_code=201)
def create_student(student: StudentCreate):
    with db_cursor() as (connection, cursor):
        cursor.execute("SELECT id FROM students WHERE email = %s", (student.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Student email already exists")

        cursor.execute("""
            INSERT INTO students
            (name, email, phone, course, graduation_year, percentage, github_url, linkedin_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student.name.strip(),
            student.email,
            student.phone,
            student.course.strip(),
            student.graduation_year,
            student.percentage,
            str(student.github_url) if student.github_url else None,
            str(student.linkedin_url) if student.linkedin_url else None,
        ))
        connection.commit()
        return {"message": "Student created successfully", "student_id": cursor.lastrowid}
