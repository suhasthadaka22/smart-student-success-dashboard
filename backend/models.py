from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    # Logical student_id like "1", "2", "3", "4", "5"
    student_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    # foreign key-ish, but we’ll keep it simple: just store student_id as string
    student_id = Column(String, index=True, nullable=False)
    course_code = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    total_classes = Column(Integer, nullable=False)
    attended = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)  # in percentage


class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    course_code = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    exam_type = Column(String, nullable=False)  # Mid-1, Mid-2, Assignment, etc.
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    topic_tags = Column(String, nullable=True)  # comma-separated topics
class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    semester = Column(Integer, nullable=False)
    sgpa = Column(Float, nullable=False)
    cgpa = Column(Float, nullable=False)


class LibraryResource(Base):
    __tablename__ = "library_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # PDF, YouTube, Notes, etc.
    url = Column(String, nullable=False)
    course_code = Column(String, nullable=True)  # DBMS, OS, DSA
    tags = Column(String, nullable=True)        # comma-separated
    description = Column(String, nullable=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=True)       # simple string like "2025-01-15"
    category = Column(String, nullable=True)   # Workshop, Hackathon, Seminar
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    recommended_for = Column(String, nullable=True)  # e.g. "low DBMS", "AI/ML"
    tags = Column(String, nullable=True)             # comma-separated
