import sys
import os

# Make project root importable so we can import backend + frontend packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit_option_menu import option_menu  # sidebar nav

from backend.database import SessionLocal
from backend.crud import (
    init_db,
    ensure_seed_data,
    get_student_by_student_id,
    get_attendance_for_student,
    get_marks_for_student,
    get_results_for_student,
    get_all_library_resources,
    get_all_events,
)

from frontend.components.layout import (
    show_profile_page,
    show_dashboard,
    show_attendance_page,
    show_marks_page,
    show_insights_page,
    show_mentor_page,
)



def get_db_session():
    return SessionLocal()


def main():
    st.set_page_config(
        page_title="Smart Student Success Dashboard",
        page_icon="🎓",
        layout="wide",
    )

    # ---- Session state for auth ----
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.student_id = None

    db = get_db_session()
    init_db()
    ensure_seed_data(db)

    # ---- Login Page ----
    if not st.session_state.logged_in:
        st.title("🎓 Student Login")
        st.write("Demo login: use your `student_id` as both username and password.")

        student_id_input = st.text_input("Student ID", key="login_student_id")
        password_input = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            student = get_student_by_student_id(db, student_id_input)
            if student and password_input == student_id_input:
                st.session_state.logged_in = True
                st.session_state.student_id = student_id_input
                st.success(f"Welcome, {student.name}!")
                st.rerun()
            else:
                st.error("Invalid credentials. Hint: student_id == password for demo.")

        db.close()
        return

    # ---- Logged-in student context ----
    logged_in_student_id = st.session_state.student_id
    student = get_student_by_student_id(db, logged_in_student_id)

    if not student:
        st.error("Logged-in student not found in the database.")
        db.close()
        return

    attendance = get_attendance_for_student(db, logged_in_student_id)
    marks = get_marks_for_student(db, logged_in_student_id)
    results = get_results_for_student(db, logged_in_student_id)
    library_resources = get_all_library_resources(db)
    events = get_all_events(db)

    # ---- Sidebar: navigation + logout (profile moved to its own page) ----
    with st.sidebar:
        page = option_menu(
            "Navigation",
            ["Profile", "Dashboard", "Attendance", "Marks", "Insights", "AI Mentor"],
            icons=[
                "person-circle",      # Profile
                "speedometer2",       # Dashboard
                "calendar-check",     # Attendance
                "bar-chart-line",     # Marks
                "lightbulb",          # Insights
                "chat-dots",          # AI Mentor
            ],
            menu_icon="cast",
            default_index=1,  # default to Dashboard
            styles={
                "container": {"padding": "0!important"},
                "icon": {"font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                # 👇 Highlight color: #0068c9
                "nav-link-selected": {
                    "background-color": "#0068c9",
                    "color": "white",
                },
            },
        )

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.rerun()

    # ---- Main title ----
    st.title("🎓 Smart Student Success Dashboard")
    st.caption("GenAI-powered student mentor using SQLite + Ollama + LangChain + RAG")

    # ---- Page router ----
    if page == "Profile":
        show_profile_page(student, attendance, marks, results)

    elif page == "Dashboard":
        show_dashboard(student, attendance, marks)

    elif page == "Attendance":
        show_attendance_page(student, attendance)

    elif page == "Marks":
        show_marks_page(student, marks)

    elif page == "Insights":
        show_insights_page(student, marks, results, library_resources, events)

    elif page == "AI Mentor":
        show_mentor_page(db, logged_in_student_id)

    db.close()


if __name__ == "__main__":
    main()
