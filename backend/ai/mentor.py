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

    # 2. Choose appropriate student context
    if query_type == "attendance":
        student_context = build_attendance_context(session, student_id)
    elif query_type in ("marks", "gpa"):
        student_context = build_marks_context(session, student_id)
    else:
        student_context = build_full_student_context(session, student_id)

    # 3. Retrieve relevant docs via RAG
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    # For LangChain >= 0.3, retrievers are Runnables
    docs = retriever.invoke(user_query)   # ✅ returns list[Document]
    rag_context = "\n\n".join(d.page_content for d in docs)

    # 4. Build system prompt with specialization
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

VERY IMPORTANT RULES (do NOT break these):
- You MUST NOT invent or change any numeric values (percentages, number of classes, scores).
- Only use the exact numbers and phrases that appear in "Student data" above for attendance and marks.
- Especially for attendance, when you talk about "how many more classes" a student needs,
  you must copy the phrase after "needs approx" from the student data WITHOUT changing the number.
- If a number is not provided in Student data or College resources, say "not specified" instead of guessing.
- Do not include any closing statements, sign-offs, signatures, or placeholders such as [Your Name] or [Your Position]. End the response naturally.
- Structure the answer with clear sections and bullet points so the student can follow the action steps easily.
"""

    llm = get_chat_llm()  # or whatever model you configured

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query),
    ]

    response = llm.invoke(messages)
    answer_text = response.content.strip()
    return answer_text
