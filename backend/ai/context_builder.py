# backend/ai/context_builder.py

from typing import List
from sqlalchemy.orm import Session

from backend.crud import (
    get_student_by_student_id,
    get_attendance_for_student,
    get_marks_for_student,
)
from backend.ai.attendance_utils import compute_attendance_insights


def _format_attendance_lines(attendance_records) -> List[str]:
    lines = []
    for a in attendance_records:
        pct, needed = compute_attendance_insights(a)
        lines.append(
            f"- {a.course_code} ({a.course_name}): "
            f"{a.attended}/{a.total_classes} classes "
            f"({pct:.1f}%), needs approx {needed} more continuous classes "
            f"to reach {a.threshold}% attendance."
        )
    return lines


def _format_marks_lines(marks_records) -> List[str]:
    lines = []
    for m in marks_records:
        if m.max_score > 0:
            perc = (m.score / m.max_score) * 100
        else:
            perc = 0.0
        topics = m.topic_tags or ""
        lines.append(
            f"- {m.course_code} {m.exam_type}: {m.score}/{m.max_score} "
            f"({perc:.1f}%), topics: {topics}"
        )
    return lines


def build_attendance_context(session: Session, student_id: str) -> str:
    """Context string focusing only on attendance."""
    student = get_student_by_student_id(session, student_id)
    attendance = get_attendance_for_student(session, student_id)

    lines = []
    lines.append(f"Student: {student.name} (ID: {student.student_id})")
    lines.append(
        f"Branch: {student.branch}, Semester: {student.semester}, Section: {student.section}"
    )

    lines.append("\nAttendance:")
    if not attendance:
        lines.append("No attendance data.")
    else:
        lines.extend(_format_attendance_lines(attendance))

    return "\n".join(lines)


def build_marks_context(session: Session, student_id: str) -> str:
    """Context string focusing only on marks/performance."""
    student = get_student_by_student_id(session, student_id)
    marks = get_marks_for_student(session, student_id)

    lines = []
    lines.append(f"Student: {student.name} (ID: {student.student_id})")
    lines.append(
        f"Branch: {student.branch}, Semester: {student.semester}, Section: {student.section}"
    )

    lines.append("\nMarks:")
    if not marks:
        lines.append("No marks data.")
    else:
        lines.extend(_format_marks_lines(marks))

    return "\n".join(lines)


def build_full_student_context(session: Session, student_id: str) -> str:
    """Attendance + marks, for general questions."""
    student = get_student_by_student_id(session, student_id)
    attendance = get_attendance_for_student(session, student_id)
    marks = get_marks_for_student(session, student_id)

    lines = []
    lines.append(f"Student: {student.name} (ID: {student.student_id})")
    lines.append(
        f"Branch: {student.branch}, Semester: {student.semester}, Section: {student.section}"
    )

    lines.append("\nAttendance:")
    if not attendance:
        lines.append("No attendance data.")
    else:
        lines.extend(_format_attendance_lines(attendance))

    lines.append("\nMarks:")
    if not marks:
        lines.append("No marks data.")
    else:
        lines.extend(_format_marks_lines(marks))

    return "\n".join(lines)


# Backwards compatibility, if other code still imports this name
def build_student_context(session: Session, student_id: str) -> str:
    return build_full_student_context(session, student_id)
