from fastapi import APIRouter, HTTPException

from ..database import db_cursor
from ..schemas import CompanyCreate

router = APIRouter(prefix="/api/companies", tags=["Companies"])


@router.get("")
def list_companies():
    with db_cursor() as (_, cursor):
        cursor.execute("""
            SELECT id, name, location, website, description, created_at
            FROM companies
            ORDER BY name
        """)
        return cursor.fetchall()


@router.post("", status_code=201)
def create_company(company: CompanyCreate):
    with db_cursor() as (connection, cursor):
        cursor.execute("""
            INSERT INTO companies (name, location, website, description)
            VALUES (%s, %s, %s, %s)
        """, (
            company.name.strip(),
            company.location.strip(),
            str(company.website) if company.website else None,
            company.description,
        ))
        connection.commit()
        return {"message": "Company created successfully", "company_id": cursor.lastrowid}


@router.get("/{company_id}")
def get_company(company_id: int):
    with db_cursor() as (_, cursor):
        cursor.execute("SELECT * FROM companies WHERE id = %s", (company_id,))
        company = cursor.fetchone()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company
