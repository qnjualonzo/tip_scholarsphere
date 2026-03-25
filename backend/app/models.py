from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

# Organizational Tables
class Campus(SQLModel, table=True):
    __tablename__ = "campuses"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    address: Optional[str] = None
    is_active: bool = Field(default=True)


class College(SQLModel, table=True):
    __tablename__ = "colleges"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    campus_id: UUID = Field(foreign_key="campuses.id")


class Department(SQLModel, table=True):
    __tablename__ = "departments"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    college_id: UUID = Field(foreign_key="colleges.id")


class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    is_active: bool = Field(default=True)


class SchoolYear(SQLModel, table=True):
    __tablename__ = "school_years"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    start_year: int
    end_year: int
    label: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)


class Semester(SQLModel, table=True):
    __tablename__ = "semesters"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    sequence_order: int = Field(default=1)
    is_active: bool = Field(default=True)


class ResearchType(SQLModel, table=True):
    __tablename__ = "research_types"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    is_active: bool = Field(default=True)


class ResearchOutputType(SQLModel, table=True):
    __tablename__ = "research_output_types"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    research_type_id: Optional[UUID] = Field(default=None, foreign_key="research_types.id")
    description: Optional[str] = None
    is_active: bool = Field(default=True)


class Author(SQLModel, table=True):
    __tablename__ = "authors"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: str = Field(index=True)
    email: Optional[str] = Field(default=None, index=True)
    department_id: Optional[UUID] = Field(default=None, foreign_key="departments.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# User Table
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    role_id: Optional[UUID] = Field(default=None, foreign_key="roles.id")
    department_id: Optional[UUID] = Field(default=None, foreign_key="departments.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
