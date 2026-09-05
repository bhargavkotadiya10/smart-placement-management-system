# Smart Placement Management System

A web-based placement management application built to manage students, companies, job opportunities, applications, and interviews.

## Features

- Dashboard with placement statistics
- Student profile creation and listing
- Company management
- Job opening management
- Job search and filtering
- Student job applications
- Duplicate-application prevention
- Application status workflow
- Interview scheduling and tracking
- REST API with interactive Swagger documentation
- MySQL relational database
- Environment-based database configuration
- Basic API test

## Architecture

Browser → FastAPI REST API → MySQL

The frontend is served by FastAPI at `/app`.

## Project Structure

```text
SmartPlacementSystem/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       ├── companies.py
│   │       ├── jobs.py
│   │       ├── students.py
│   │       ├── applications.py
│   │       └── interviews.py
│   ├── tests/
│   │   └── test_health.py
│   └── requirements.txt
├── database/
│   ├── schema.sql
│   └── seed.sql
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── .env.example
├── .gitignore
└── README.md
```

## Setup on Windows

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

3. Create a `.env` file in the project root based on `.env.example` and add your local MySQL password.
4. In MySQL, run `database/schema.sql`.
5. Optional: run `database/seed.sql` for sample companies/jobs.
6. Start the server from the project root:

```powershell
uvicorn backend.app.main:app --reload
```

7. Open the application:

```text
http://127.0.0.1:8000/app/
```

8. Open API documentation:

```text
http://127.0.0.1:8000/docs
```

## Database Security Note

Never commit `.env` or real passwords to GitHub. Use `.env.example` as a template.
