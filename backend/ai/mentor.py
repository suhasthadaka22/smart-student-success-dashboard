# backend/ai/mentor.py

from sqlalchemy.orm import Session

from backend.ai.context_builder import (
    build_attendance_context,
    build_marks_context,
    build_full_student_context,
)
from backend.ai.vector_store import get_vectorstore
from backend.ai.llm_client import get_chat_llm
from langchain_core.messages import SystemMessage, HumanMessage

def detect_query_type(user_query: str) -> str:
    """Very simple intent detection based on keywords."""
    q = user_query.lower()

    if "attendance" in q or "classes" in q or "75%" in q:
        return "attendance"

    if "mark" in q or "score" in q or "exam" in q or "weak subject" in q or "improve my dbms" in q:
        return "marks"

    if "gpa" in q or "cgpa" in q or "sgpa" in q:
        return "gpa"

    if "event" in q or "workshop" in q or "hackathon" in q or "seminar" in q:
        return "events"

    if "resource" in q or "library" in q or "notes" in q or "youtube" in q:
        return "resources"

    return "general"


def build_focus_instructions(query_type: str) -> str:
    """Extra rules to specialize the answer based on the query type."""
    if query_type == "attendance":
        return (
            "The student is asking specifically about attendance. "
            "Focus ONLY on attendance: percentages, which subjects are at risk, "
            "and how many more classes they should attend to reach the threshold. "
            "Do NOT discuss marks, GPA, or subjects' scores unless the user explicitly mentions them."
        )
    elif query_type in ("marks", "gpa"):
        return (
            "The student is asking about marks, scores, or GPA. "
            "Focus on identifying strong and weak subjects, explaining marks, "
            "and suggesting a targeted study plan with topics and resources. "
            "Only mention attendance briefly if it is critical to the answer."
        )
    elif query_type in ("events", "resources"):
        return (
            "The student is asking about resources or events. "
            "Focus on recommending the most relevant digital library resources and events/workshops "
            "that match the student's weak areas or interests."
        )
    else:
        return (
            "The student is asking a general question. "
            "Give a balanced answer that considers attendance, marks, and available resources/events, "
            "but keep the answer concise and structured."
        )


def genai_mentor_answer(session: Session, student_id: str, user_query: str) -> str:
    # 1. Detect intent
    query_type = detect_query_type(user_query)

    # 2. Handle GENERAL queries separately (KEY CHANGE)
    if query_type == "general":
        # Light academic summary only (2–3 lines worth of data)
        academic_hint = build_attendance_context(session, student_id)

        system_prompt = f"""
You are a helpful and neutral AI assistant.

Answer the user's question clearly and factually.

After answering the question, add a SHORT academic note
(ONLY 2–3 lines) using the information below.
Do NOT give detailed breakdowns, percentages, or long lists.

Academic summary (for brief closing only):
{academic_hint}

Rules:
- The main answer must NOT be about academics.
- The academic part must be concise (max 2–3 lines).
- Do NOT invent or change any numbers.
- Do NOT mention marks unless explicitly asked.
- Do NOT add signatures or placeholders.
"""

        llm = get_chat_llm()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query),
        ]
        response = llm.invoke(messages)
        return response.content.strip()

    # -------------------------------
    # Academic queries (existing logic)
    # -------------------------------

    if query_type == "attendance":
        student_context = build_attendance_context(session, student_id)
    elif query_type in ("marks", "gpa"):
        student_context = build_marks_context(session, student_id)
    else:
        student_context = build_full_student_context(session, student_id)

    # 3. RAG only for academic queries
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(user_query)
    rag_context = "\n\n".join(d.page_content for d in docs)

    focus_instructions = build_focus_instructions(query_type)

    system_prompt = f"""
You are a friendly but strict college mentor AI.

Student data:
{student_context}

College rules / resources (retrieved via RAG):
{rag_context}

User's question:
\"\"\"{user_query}\"\"\"

{focus_instructions}

VERY IMPORTANT RULES:
- You MUST NOT invent or change any numeric values.
- Use only numbers present in Student data or RAG context.
- Do not include signatures or placeholders.
- Structure the answer clearly with bullet points and sections.
"""

    llm = get_chat_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query),
    ]

    response = llm.invoke(messages)
    return response.content.strip()
