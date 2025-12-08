from sqlalchemy.orm import Session

from .database import Base, engine
from .models import Student, Attendance, Mark, Result, LibraryResource, Event


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def ensure_seed_data(session: Session):
    """
    Seed demo data once.
    We only insert data into a table if it's empty.
    """

    # ---------- Students ----------
    if session.query(Student).count() == 0:
        students = [
            Student(student_id="1", name="Suhas",  branch="ECE", semester=7, section="A"),
            Student(student_id="2", name="Ananya", branch="CSE", semester=7, section="A"),
            Student(student_id="3", name="Rahul",  branch="EEE", semester=7, section="B"),
            Student(student_id="4", name="Priya",  branch="ME",  semester=7, section="C"),
            Student(student_id="5", name="Aditya", branch="ECE", semester=7, section="B"),
        ]
        session.add_all(students)

    # Helper to add attendance
    def att(stu_id, code, name, total, attended, threshold=75):
        return Attendance(
            student_id=stu_id,
            course_code=code,
            course_name=name,
            total_classes=total,
            attended=attended,
            threshold=threshold,
        )

    # Helper to add marks
    def mark(stu_id, code, name, exam_type, score, max_score, topics):
        return Mark(
            student_id=stu_id,
            course_code=code,
            course_name=name,
            exam_type=exam_type,
            score=score,
            max_score=max_score,
            topic_tags=",".join(topics),
        )

    # ---------- Attendance ----------
    if session.query(Attendance).count() == 0:
        attendance_records = [
            # 1: Suhas – low DBMS attendance, good OS, average DSA
            att("1", "DBMS", "Database Management Systems", 40, 26),
            att("1", "OS",   "Operating Systems",            35, 30),
            att("1", "DSA",  "Data Structures & Algorithms", 38, 32),

            # 2: Ananya – very good attendance
            att("2", "DBMS", "Database Management Systems", 40, 36),
            att("2", "OS",   "Operating Systems",            35, 34),
            att("2", "DSA",  "Data Structures & Algorithms", 38, 37),

            # 3: Rahul – low OS attendance
            att("3", "DBMS", "Database Management Systems", 40, 33),
            att("3", "OS",   "Operating Systems",            35, 20),
            att("3", "DSA",  "Data Structures & Algorithms", 38, 30),

            # 4: Priya – low DSA attendance
            att("4", "DBMS", "Database Management Systems", 40, 35),
            att("4", "OS",   "Operating Systems",            35, 32),
            att("4", "DSA",  "Data Structures & Algorithms", 38, 22),

            # 5: Aditya – struggling overall
            att("5", "DBMS", "Database Management Systems", 40, 24),
            att("5", "OS",   "Operating Systems",            35, 23),
            att("5", "DSA",  "Data Structures & Algorithms", 38, 21),
        ]
        session.add_all(attendance_records)

    # ---------- Marks ----------
    if session.query(Mark).count() == 0:
        marks_records = [
            # 1: Suhas
            mark("1", "DBMS", "Database Management Systems", "Mid-1", 12, 25, ["ER model", "Relational algebra"]),
            mark("1", "DBMS", "Database Management Systems", "Mid-2",  9, 25, ["Normalization", "Indexing"]),
            mark("1", "OS",   "Operating Systems",            "Mid-1", 18, 25, ["CPU scheduling", "Threads"]),
            mark("1", "DSA",  "Data Structures & Algorithms", "Mid-1", 20, 25, ["Arrays", "Linked Lists"]),

            # 2: Ananya – topper-type
            mark("2", "DBMS", "Database Management Systems", "Mid-1", 22, 25, ["ER model", "SQL basics"]),
            mark("2", "OS",   "Operating Systems",            "Mid-1", 23, 25, ["CPU scheduling", "Processes"]),
            mark("2", "DSA",  "Data Structures & Algorithms", "Mid-1", 24, 25, ["Arrays", "Recursion"]),

            # 3: Rahul – weak OS
            mark("3", "DBMS", "Database Management Systems", "Mid-1", 19, 25, ["ER model", "SQL basics"]),
            mark("3", "OS",   "Operating Systems",            "Mid-1", 10, 25, ["CPU scheduling", "Deadlocks"]),
            mark("3", "DSA",  "Data Structures & Algorithms", "Mid-1", 17, 25, ["Stacks", "Queues"]),

            # 4: Priya – weak DSA
            mark("4", "DBMS", "Database Management Systems", "Mid-1", 20, 25, ["Normalization", "SQL queries"]),
            mark("4", "OS",   "Operating Systems",            "Mid-1", 19, 25, ["Processes", "Threads"]),
            mark("4", "DSA",  "Data Structures & Algorithms", "Mid-1", 11, 25, ["Trees", "Recursion"]),

            # 5: Aditya – struggling in all
            mark("5", "DBMS", "Database Management Systems", "Mid-1", 11, 25, ["SQL basics", "Joins"]),
            mark("5", "OS",   "Operating Systems",            "Mid-1",  9, 25, ["CPU scheduling", "Processes"]),
            mark("5", "DSA",  "Data Structures & Algorithms", "Mid-1", 10, 25, ["Arrays", "Linked Lists"]),
        ]
        session.add_all(marks_records)

    # ---------- GPA / Results ----------
    if session.query(Result).count() == 0:
        results = [
            # student_id, semester, sgpa, cgpa
            Result(student_id="1", semester=4, sgpa=7.5, cgpa=7.5),
            Result(student_id="1", semester=5, sgpa=7.8, cgpa=7.6),
            Result(student_id="1", semester=6, sgpa=8.0, cgpa=7.8),
            Result(student_id="1", semester=7, sgpa=0.0, cgpa=7.8),

            Result(student_id="2", semester=4, sgpa=8.8, cgpa=8.8),
            Result(student_id="2", semester=5, sgpa=9.0, cgpa=8.9),
            Result(student_id="2", semester=6, sgpa=9.2, cgpa=9.0),
            Result(student_id="2", semester=7, sgpa=0.0, cgpa=9.0),

            Result(student_id="3", semester=4, sgpa=7.0, cgpa=7.0),
            Result(student_id="3", semester=5, sgpa=7.2, cgpa=7.1),
            Result(student_id="3", semester=6, sgpa=7.4, cgpa=7.2),
            Result(student_id="3", semester=7, sgpa=0.0, cgpa=7.2),

            Result(student_id="4", semester=4, sgpa=7.6, cgpa=7.6),
            Result(student_id="4", semester=5, sgpa=7.3, cgpa=7.5),
            Result(student_id="4", semester=6, sgpa=7.1, cgpa=7.3),
            Result(student_id="4", semester=7, sgpa=0.0, cgpa=7.3),

            Result(student_id="5", semester=4, sgpa=6.5, cgpa=6.5),
            Result(student_id="5", semester=5, sgpa=6.8, cgpa=6.6),
            Result(student_id="5", semester=6, sgpa=6.9, cgpa=6.7),
            Result(student_id="5", semester=7, sgpa=0.0, cgpa=6.7),
        ]
        session.add_all(results)

    # ---------- Library Resources ----------
    if session.query(LibraryResource).count() == 0:
        resources = [
            LibraryResource(
                title="DBMS Lecture Notes PDF",
                type="PDF",
                url="https://example.com/dbms-notes.pdf",
                course_code="DBMS",
                tags="dbms,notes,pdf,normalization,sql",
                description="Concise DBMS notes covering ER diagrams, normalization, SQL queries and joins.",
            ),
            LibraryResource(
                title="DBMS YouTube Playlist",
                type="YouTube",
                url="https://youtube.com/playlist?list=DBMS_PLAYLIST",
                course_code="DBMS",
                tags="dbms,youtube,sql,joins,indexing",
                description="Video playlist focusing on SQL basics, joins, indexing, and query optimization.",
            ),
            LibraryResource(
                title="OS Unit-2 Notes",
                type="PDF",
                url="https://example.com/os-unit2.pdf",
                course_code="OS",
                tags="os,notes,cpu scheduling,threads",
                description="Operating Systems notes for CPU scheduling, processes and threads.",
            ),
            LibraryResource(
                title="OS Concepts Video Series",
                type="YouTube",
                url="https://youtube.com/playlist?list=OS_PLAYLIST",
                course_code="OS",
                tags="os,youtube,deadlocks,synchronization",
                description="Video series explaining deadlocks, synchronization, and process management.",
            ),
            LibraryResource(
                title="DSA Cheat Sheet PDF",
                type="PDF",
                url="https://example.com/dsa-cheatsheet.pdf",
                course_code="DSA",
                tags="dsa,cheatsheet,arrays,linked lists,trees",
                description="Quick revision cheat sheet for core data structures topics.",
            ),
            LibraryResource(
                title="DSA Coding Playlist",
                type="YouTube",
                url="https://youtube.com/playlist?list=DSA_PLAYLIST",
                course_code="DSA",
                tags="dsa,youtube,coding,practice",
                description="Coding-focused playlist implementing data structures and solving problems.",
            ),
        ]
        session.add_all(resources)

    # ---------- Events ----------
    if session.query(Event).count() == 0:
        events = [
            Event(
                title="DBMS Crash Course Workshop",
                date="2025-01-15",
                category="Workshop",
                location="Lab-1",
                description="Hands-on sessions on SQL, joins, indexing, and query optimization.",
                recommended_for="low DBMS, improve SQL",
                tags="dbms,sql,workshop",
            ),
            Event(
                title="Operating Systems Lab Bootcamp",
                date="2025-01-20",
                category="Bootcamp",
                location="Lab-2",
                description="Practical CPU scheduling and synchronization problems.",
                recommended_for="low OS, weak in CPU scheduling or deadlocks",
                tags="os,bootcamp,scheduling",
            ),
            Event(
                title="Coding Club DSA Series",
                date="Every Saturday",
                category="Club",
                location="CSE Block",
                description="Weekly sessions on arrays, linked lists, stacks, queues, and trees.",
                recommended_for="improve DSA fundamentals",
                tags="dsa,coding,club",
            ),
        ]
        session.add_all(events)

    session.commit()


# ---------- Query helper functions ----------

def get_all_students(session: Session):
    return session.query(Student).order_by(Student.name).all()


def get_student_by_student_id(session: Session, student_id: str):
    return session.query(Student).filter(Student.student_id == student_id).first()


def get_attendance_for_student(session: Session, student_id: str):
    return session.query(Attendance).filter(Attendance.student_id == student_id).all()


def get_marks_for_student(session: Session, student_id: str):
    return session.query(Mark).filter(Mark.student_id == student_id).all()


def get_results_for_student(session: Session, student_id: str):
    return (
        session.query(Result)
        .filter(Result.student_id == student_id)
        .order_by(Result.semester)
        .all()
    )


def get_all_library_resources(session: Session):
    return session.query(LibraryResource).all()


def get_all_events(session: Session):
    return session.query(Event).all()

def get_results_for_student(session, student_id: str):
    from .models import Result
    return (
        session.query(Result)
        .filter(Result.student_id == student_id)
        .order_by(Result.semester)
        .all()
    )
