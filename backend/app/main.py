from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from app.database import create_db_and_tables, get_session
from app.models import (
    Author,
    Campus,
    College,
    Department,
    ResearchOutputType,
    ResearchType,
    Role,
    SchoolYear,
    Semester,
    User,
)
from app.security import create_access_token, hash_password, verify_password

app = FastAPI(title="TIP ScholarSphere API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    department_id: Optional[UUID] = None
    role_id: Optional[UUID] = None


class CampusCreate(BaseModel):
    name: str
    address: Optional[str] = None
    is_active: bool = True


class CollegeCreate(BaseModel):
    name: str
    campus_id: UUID


class DepartmentCreate(BaseModel):
    name: str
    college_id: UUID


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class AuthorCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    department_id: Optional[UUID] = None
    is_active: bool = True


class SchoolYearCreate(BaseModel):
    start_year: int
    end_year: int
    is_active: bool = True


class SemesterCreate(BaseModel):
    name: str
    sequence_order: int = 1
    is_active: bool = True


class ResearchTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class ResearchOutputTypeCreate(BaseModel):
    name: str
    research_type_id: Optional[UUID] = None
    description: Optional[str] = None
    is_active: bool = True


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Welcome to TIP ScholarSphere API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user_data.department_id:
        department = session.get(Department, user_data.department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    if user_data.role_id:
        role = session.get(Role, user_data.role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        department_id=user_data.department_id,
        role_id=user_data.role_id,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"id": new_user.id, "message": "User created successfully"}


@app.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/campuses")
def list_campuses(session: Session = Depends(get_session)):
    return session.exec(select(Campus)).all()


@app.post("/campuses", status_code=status.HTTP_201_CREATED)
def create_campus(data: CampusCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Campus).where(Campus.name == data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Campus already exists")
    campus = Campus(name=data.name, address=data.address, is_active=data.is_active)
    session.add(campus)
    session.commit()
    session.refresh(campus)
    return campus


@app.get("/colleges")
def list_colleges(session: Session = Depends(get_session)):
    return session.exec(select(College)).all()


@app.post("/colleges", status_code=status.HTTP_201_CREATED)
def create_college(data: CollegeCreate, session: Session = Depends(get_session)):
    if not session.get(Campus, data.campus_id):
        raise HTTPException(status_code=404, detail="Campus not found")
    college = College(name=data.name, campus_id=data.campus_id)
    session.add(college)
    session.commit()
    session.refresh(college)
    return college


@app.get("/departments")
def list_departments(session: Session = Depends(get_session)):
    return session.exec(select(Department)).all()


@app.post("/departments", status_code=status.HTTP_201_CREATED)
def create_department(data: DepartmentCreate, session: Session = Depends(get_session)):
    if not session.get(College, data.college_id):
        raise HTTPException(status_code=404, detail="College not found")
    department = Department(name=data.name, college_id=data.college_id)
    session.add(department)
    session.commit()
    session.refresh(department)
    return department


@app.get("/roles")
def list_roles(session: Session = Depends(get_session)):
    return session.exec(select(Role)).all()


@app.post("/roles", status_code=status.HTTP_201_CREATED)
def create_role(data: RoleCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Role).where(Role.name == data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    role = Role(name=data.name, description=data.description, is_active=data.is_active)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


@app.get("/authors")
def list_authors(session: Session = Depends(get_session)):
    return session.exec(select(Author)).all()


@app.post("/authors", status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorCreate, session: Session = Depends(get_session)):
    if data.department_id and not session.get(Department, data.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    author = Author(
        full_name=data.full_name,
        email=data.email,
        department_id=data.department_id,
        is_active=data.is_active,
    )
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/school-years")
def list_school_years(session: Session = Depends(get_session)):
    return session.exec(select(SchoolYear)).all()


@app.post("/school-years", status_code=status.HTTP_201_CREATED)
def create_school_year(data: SchoolYearCreate, session: Session = Depends(get_session)):
    if data.start_year >= data.end_year:
        raise HTTPException(status_code=400, detail="start_year must be less than end_year")
    label = f"{data.start_year}-{data.end_year}"
    existing = session.exec(select(SchoolYear).where(SchoolYear.label == label)).first()
    if existing:
        raise HTTPException(status_code=400, detail="School year already exists")
    school_year = SchoolYear(
        start_year=data.start_year,
        end_year=data.end_year,
        label=label,
        is_active=data.is_active,
    )
    session.add(school_year)
    session.commit()
    session.refresh(school_year)
    return school_year


@app.get("/semesters")
def list_semesters(session: Session = Depends(get_session)):
    return session.exec(select(Semester)).all()


@app.post("/semesters", status_code=status.HTTP_201_CREATED)
def create_semester(data: SemesterCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Semester).where(Semester.name == data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Semester already exists")
    semester = Semester(
        name=data.name,
        sequence_order=data.sequence_order,
        is_active=data.is_active,
    )
    session.add(semester)
    session.commit()
    session.refresh(semester)
    return semester


@app.get("/research-types")
def list_research_types(session: Session = Depends(get_session)):
    return session.exec(select(ResearchType)).all()


@app.post("/research-types", status_code=status.HTTP_201_CREATED)
def create_research_type(data: ResearchTypeCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(ResearchType).where(ResearchType.name == data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Research type already exists")
    research_type = ResearchType(
        name=data.name,
        description=data.description,
        is_active=data.is_active,
    )
    session.add(research_type)
    session.commit()
    session.refresh(research_type)
    return research_type


@app.get("/research-output-types")
def list_research_output_types(session: Session = Depends(get_session)):
    return session.exec(select(ResearchOutputType)).all()


@app.post("/research-output-types", status_code=status.HTTP_201_CREATED)
def create_research_output_type(
    data: ResearchOutputTypeCreate, session: Session = Depends(get_session)
):
    if data.research_type_id and not session.get(ResearchType, data.research_type_id):
        raise HTTPException(status_code=404, detail="Research type not found")
    existing = session.exec(
        select(ResearchOutputType).where(ResearchOutputType.name == data.name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Research output type already exists")
    output_type = ResearchOutputType(
        name=data.name,
        research_type_id=data.research_type_id,
        description=data.description,
        is_active=data.is_active,
    )
    session.add(output_type)
    session.commit()
    session.refresh(output_type)
    return output_type
