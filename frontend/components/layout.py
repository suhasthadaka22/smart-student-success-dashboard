import streamlit as st
import pandas as pd
import textwrap

from backend.ai.attendance_utils import compute_attendance_insights
from backend.ai.mentor import genai_mentor_answer


# ---------- Attendance rendering ----------

def _render_attendance_block(attendance):
    st.subheader("Attendance Overview")
    if not attendance:
        st.write("No attendance data.")
        return

    for a in attendance:
        pct, needed = compute_attendance_insights(a)
        status_emoji = "✅" if pct >= a.threshold else "⚠️"
        st.markdown(
            f"- {status_emoji} **{a.course_code} - {a.course_name}**: "
            f"{a.attended}/{a.total_classes} classes "
            f"({pct:.1f}%), needs ~**{needed}** more classes to reach {a.threshold}%"
        )

    # Attendance chart
    subjects = [a.course_code for a in attendance]
    attendance_pcts = [compute_attendance_insights(a)[0] for a in attendance]

    att_df = pd.DataFrame({
        "Subject": subjects,
        "Attendance %": attendance_pcts,
    })

    st.markdown("#### Attendance Chart")
    st.bar_chart(att_df, x="Subject", y="Attendance %")


# ---------- Marks + insights rendering ----------

def _render_marks_block(marks):
    st.subheader("Marks Overview")
    if not marks:
        st.write("No marks data.")
        return

    for m in marks:
        perc = (m.score / m.max_score) * 100 if m.max_score > 0 else 0
        topics = m.topic_tags or ""
        status_emoji = "✅" if perc >= 70 else ("⚠️" if perc >= 50 else "❌")
        st.markdown(
            f"- {status_emoji} **{m.course_code} {m.exam_type}**: "
            f"{m.score}/{m.max_score} ({perc:.1f}%), "
            f"topics: *{topics}*"
        )

    # Marks chart
    labels = [f"{m.course_code} {m.exam_type}" for m in marks]
    marks_pcts = [
        (m.score / m.max_score) * 100 if m.max_score > 0 else 0
        for m in marks
    ]

    marks_df = pd.DataFrame({
        "Exam": labels,
        "Marks %": marks_pcts,
    })

    st.markdown("#### Marks Chart")
    st.bar_chart(marks_df, x="Exam", y="Marks %")


def _compute_course_averages(marks):
    course_scores = {}
    course_names = {}
    for m in marks:
        perc = (m.score / m.max_score) * 100 if m.max_score > 0 else 0
        if m.course_code not in course_scores:
            course_scores[m.course_code] = []
            course_names[m.course_code] = m.course_name
        course_scores[m.course_code].append(perc)

    averaged = []
    for code, score_list in course_scores.items():
        avg = sum(score_list) / len(score_list)
        averaged.append((code, course_names[code], avg))

    averaged.sort(key=lambda x: x[2])
    return averaged


def _render_performance_insights(marks):
    st.markdown("#### Performance Insights")

    if not marks:
        st.write("No marks available to analyze.")
        return

    averaged = _compute_course_averages(marks)

    strong = [f"{code} ({name}) – {avg:.1f}%" for code, name, avg in averaged if avg >= 75]
    okay = [f"{code} ({name}) – {avg:.1f}%" for code, name, avg in averaged if 60 <= avg < 75]
    weak = [f"{code} ({name}) – {avg:.1f}%" for code, name, avg in averaged if avg < 60]

    if strong:
        st.markdown("**Strong in:**")
        for s in strong:
            st.markdown(f"- ✅ {s}")

    if okay:
        st.markdown("**Decent but can improve:**")
        for s in okay:
            st.markdown(f"- ⚠️ {s}")

    if weak:
        st.markdown("**Needs attention:**")
        for s in weak:
            st.markdown(f"- ❌ {s}")

    if not (strong or okay or weak):
        st.write("No marks available to analyze.")


# ---------- GPA / SGPA rendering ----------

def _render_gpa_section(results):
    st.subheader("GPA / SGPA Trend")

    if not results:
        st.write("No GPA/SGPA data available yet.")
        return

    semesters = [r.semester for r in results]
    sgpa_vals = [r.sgpa for r in results]
    cgpa_vals = [r.cgpa for r in results]

    df = pd.DataFrame({
        "Semester": semesters,
        "SGPA": sgpa_vals,
        "CGPA": cgpa_vals,
    })

    df = df.set_index("Semester")
    st.line_chart(df)


# ---------- Library rendering ----------

def _render_library_section(library_resources, marks):
    st.subheader("Digital Library")

    if not library_resources:
        st.write("No library resources available.")
        return

    search = st.text_input(
        "Search resources (title, course, tags):",
        key="library_search",
        placeholder="e.g., DBMS SQL, OS deadlocks, DSA trees...",
    )

    # Basic filter by weak subjects if any
    averaged = _compute_course_averages(marks) if marks else []
    weak_codes = [code for code, _name, avg in averaged if avg < 60]

    resources = library_resources
    if search.strip():
        q = search.lower()
        resources = [
            r for r in resources
            if q in (r.title or "").lower()
            or q in (r.course_code or "").lower()
            or q in (r.tags or "").lower()
            or q in (r.description or "").lower()
        ]

    if weak_codes and not search.strip():
        # auto-prioritize resources from weakest subjects
        resources = [
            r for r in resources
            if (r.course_code or "") in weak_codes
        ] or resources

    if not resources:
        st.write("No matching resources found.")
        return

    for r in resources:
        st.markdown(
            f"**{r.title}**  \n"
            f"Type: *{r.type}* · Course: `{r.course_code or 'N/A'}`  \n"
            f"{r.description or ''}  \n"
            f"[Open link]({r.url})"
        )
        st.markdown("---")


# ---------- Events rendering ----------

def _render_events_section(events, marks):
    st.subheader("Recommended Events & Workshops")

    if not events:
        st.write("No upcoming events found.")
        return

    averaged = _compute_course_averages(marks) if marks else []
    weak_codes = [code for code, _name, avg in averaged if avg < 60]

    # Simple relevance scoring: events mentioning weak subjects get priority
    def score_event(ev):
        tags = (ev.tags or "").lower()
        desc = (ev.description or "").lower()
        score = 0
        for code in weak_codes:
            if code.lower() in tags or code.lower() in desc:
                score += 1
        return score

    sorted_events = sorted(events, key=score_event, reverse=True)

    for ev in sorted_events:
        st.markdown(f"**{ev.title}**")
        meta_line = []
        if ev.date:
            meta_line.append(f"📅 {ev.date}")
        if ev.location:
            meta_line.append(f"📍 {ev.location}")
        if ev.category:
            meta_line.append(f"🏷 {ev.category}")
        if meta_line:
            st.markdown(" · ".join(meta_line))
        if ev.description:
            st.markdown(ev.description)
        if ev.recommended_for:
            st.markdown(f"*Recommended for:* {ev.recommended_for}")
        st.markdown("---")


# ---------- Page-level render functions ----------

def show_dashboard(student, attendance, marks):
    col1, col2 = st.columns([2, 3])

    with col1:
        _render_attendance_block(attendance)

    with col2:
        _render_marks_block(marks)
        _render_performance_insights(marks)


def show_attendance_page(student, attendance):
    _render_attendance_block(attendance)


def show_marks_page(student, marks):
    _render_marks_block(marks)
    _render_performance_insights(marks)


def show_insights_page(student, marks, results, library_resources, events):
    # GPA / SGPA
    _render_gpa_section(results)

    # Performance insights based on marks
    _render_performance_insights(marks)

    st.markdown("---")

    # Library section
    _render_library_section(library_resources, marks)

    st.markdown("---")

    # Events section
    _render_events_section(events, marks)


def show_mentor_page(db, student_id):
    st.header("🧠 GenAI Mentor")

    default_q = (
        "Explain my academic situation and give a clear plan to "
        "improve my weak subjects and maintain good attendance."
    )

    user_query = st.text_area(
        "Ask anything about your performance, attendance, or what to focus on:",
        value=default_q,
        height=120,
    )

    st.markdown("**Quick questions:**")
    qcol1, qcol2, qcol3 = st.columns(3)

    quick_action = None
    with qcol1:
        if st.button("📉 Fix my attendance"):
            quick_action = (
                "I am only asking about attendance. "
                "Look at my attendance in each subject, tell me which ones are below or close to 75%, "
                "and give a very concrete plan on how to fix my attendance. "
                "Do not talk about marks or GPA, just attendance."
            )

    with qcol2:
        if st.button("📚 Improve my weakest subject"):
            quick_action = (
                "I am only asking about marks and weak subjects. "
                "Look at my marks, identify my weakest subject, explain why it is weak, "
                "and give a focused study plan with topics and digital library resources. "
                "Do not talk about attendance unless it is absolutely necessary."
            )

    with qcol3:
        if st.button("🗓 7-day study plan"):
            quick_action = (
                "Using my current marks and attendance, create a realistic 7-day study plan "
                "that focuses more on my weakest subject but still maintains other subjects. "
                "Keep the plan specific and actionable."
            )

    mentor_answer = None

    if quick_action:
        with st.spinner("Mentor is analyzing your data + college resources..."):
            mentor_answer = genai_mentor_answer(db, student_id, quick_action)

    elif st.button("Ask Mentor"):
        if not user_query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Mentor is analyzing your data + college resources..."):
                mentor_answer = genai_mentor_answer(db, student_id, user_query)

    if mentor_answer:
        st.subheader("Mentor's Response")
        st.markdown(mentor_answer)


import streamlit as st
import pandas as pd
# ... your other imports stay as-is ...


def show_profile_page(student, attendance, marks, results):
    st.subheader("Student Profile")

    # ---- Quick stats for the metrics row ----
    total_subjects = len({a.course_code for a in attendance}) if attendance else 0

    avg_attendance = None
    if attendance:
        pcts = [
            (a.attended / a.total_classes) * 100
            for a in attendance
            if a.total_classes > 0
        ]
        if pcts:
            avg_attendance = sum(pcts) / len(pcts)

    latest_cgpa = None
    if results:
        non_zero = [r.cgpa for r in results if r.cgpa > 0]
        latest_cgpa = non_zero[-1] if non_zero else results[-1].cgpa

    # ---- Layout: left (profile) + right (metrics & summary) ----
    col1, col2 = st.columns([2, 3])

    # LEFT: basic profile info
    with col1:
        st.markdown(f"### 👤 {student.name}")
        st.markdown(f"- **Student ID:** `{student.student_id}`")
        st.markdown(f"- **Branch:** {student.branch}")
        st.markdown(f"- **Semester:** {student.semester}")
        st.markdown(f"- **Section:** {student.section}")

        st.markdown("---")
        st.markdown("**Program**")
        st.markdown(f"{student.branch} - B.Tech")

    # RIGHT: metrics & summary
    with col2:
        st.markdown("#### At a Glance")

        mcol1, mcol2, mcol3 = st.columns(3)

        with mcol1:
            st.metric("Subjects", value=total_subjects if total_subjects else "—")

        with mcol2:
            if avg_attendance is not None:
                st.metric("Avg Attendance", f"{avg_attendance:.1f}%")
            else:
                st.metric("Avg Attendance", "—")

        with mcol3:
            if latest_cgpa is not None:
                st.metric("Latest CGPA", f"{latest_cgpa:.2f}")
            else:
                st.metric("Latest CGPA", "—")

        st.markdown("---")
        st.markdown("#### Quick Summary")
        st.write(
            "Use the navigation menu on the left to explore your "
            "attendance, marks, GPA trends, recommended digital resources, "
            "upcoming events, and to chat with the AI Mentor."
        )
