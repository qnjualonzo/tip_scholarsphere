# TIP ScholarSphere - Member Scope Completion Report

## Overview
This repository now covers the assigned Member 1 scope (database normalization and table connections) and provides temporary backend APIs needed to unblock login/registration frontend work while waiting for teammate-owned API work.

## Assigned scope and completion status

### Member 1 scope
- Login and Registration: **Implemented**
- Campus: **Implemented**
- College: **Implemented**
- Department: **Implemented**
- Role: **Implemented**
- Author: **Implemented**
- School Year (schyear): **Implemented**
- Semester: **Implemented**
- Research Type: **Implemented**
- Research Output Type: **Implemented**

### Member 2 scope
- Research Evaluation: **Not implemented in this branch** (teammate scope)

### Member 3 scope
- Presentation, Publication, and another table: **Not implemented in this branch** (teammate scope)

## Database normalization and table connections
Core normalized hierarchy and links:
- `campuses` -> `colleges` via `colleges.campus_id`
- `colleges` -> `departments` via `departments.college_id`
- `departments` -> `users` via `users.department_id`
- `roles` -> `users` via `users.role_id`
- `departments` -> `authors` via `authors.department_id`
- `research_types` -> `research_output_types` via `research_output_types.research_type_id`

All IDs use UUID primary keys.

## Backend API endpoints currently available

### Auth
- `POST /register`
- `POST /login`

### Member 1 lookup and master data
- Campuses: `GET /campuses`, `POST /campuses`
- Colleges: `GET /colleges`, `POST /colleges`
- Departments: `GET /departments`, `POST /departments`
- Roles: `GET /roles`, `POST /roles`
- Authors: `GET /authors`, `POST /authors`
- School Years: `GET /school-years`, `POST /school-years`
- Semesters: `GET /semesters`, `POST /semesters`
- Research Types: `GET /research-types`, `POST /research-types`
- Research Output Types: `GET /research-output-types`, `POST /research-output-types`

### Health and root
- `GET /health`
- `GET /`

## Frontend status
- Login page exists and calls `POST /login`
- Registration page exists and calls `POST /register`
- Routes configured in `frontend/src/App.jsx`
- API base URL is now configurable via `VITE_API_BASE_URL`

## Security and push-readiness updates
- Removed hardcoded DB credentials from backend code.
- Removed hardcoded JWT secret from backend code.
- Added environment-based configuration:
  - `backend/.env.example`
  - `frontend/.env.example`
- Added ignores:
  - `backend/.env`
  - `frontend/.env`

## Validation status
Validation script (`python validate.py`) result:
- Backend: PASS
- Frontend: PASS

## How to run

### Backend
```powershell
cd F:\Users\me\tip_scholarsphere\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```

### Frontend
```powershell
cd F:\Users\me\tip_scholarsphere\frontend
npm install
copy .env.example .env
npm run dev
```

## Suggested talking points for supervisor
- The assigned Member 1 tables are normalized and connected with foreign keys.
- Login/registration is fully wired backend-to-frontend and validated.
- Temporary APIs were implemented to unblock frontend progress while teammate APIs are pending.
- Secret handling was refactored to environment variables for safe GitHub push.
- Remaining domain APIs (Research Evaluation, Presentation, Publication, and related tables) stay with assigned teammates and can be integrated next.
