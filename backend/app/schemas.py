from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, field_validator


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    phone: str | None = Field(default=None, max_length=20)
    course: str = Field(min_length=2, max_length=50)
    graduation_year: int | None = Field(default=None, ge=2020, le=2100)
    percentage: float | None = Field(default=None, ge=0, le=100)
    github_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    location: str = Field(min_length=2, max_length=100)
    website: HttpUrl | None = None
    description: str | None = None


class JobCreate(BaseModel):
    company_id: int = Field(gt=0)
    title: str = Field(min_length=2, max_length=150)
    location: str = Field(min_length=2, max_length=100)
    internship_duration: str | None = Field(default=None, max_length=50)
    stipend: str | None = Field(default=None, max_length=50)
    salary: str | None = Field(default=None, max_length=50)
    description: str | None = None
    skills: str | None = None
    min_percentage: float | None = Field(default=None, ge=0, le=100)
    openings: int = Field(default=1, ge=1, le=1000)


class ApplicationCreate(BaseModel):
    student_id: int = Field(gt=0)
    job_id: int = Field(gt=0)


class StatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        allowed = {"Applied", "Shortlisted", "Interview", "Selected", "Rejected"}
        if value not in allowed:
            raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
        return value


class InterviewCreate(BaseModel):
    application_id: int = Field(gt=0)
    round_name: str = Field(min_length=2, max_length=100)
    scheduled_at: datetime
    mode: str = Field(min_length=2, max_length=30)
    notes: str | None = None
