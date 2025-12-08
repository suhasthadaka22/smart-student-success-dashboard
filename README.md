<h1 align="center">🎓 Smart Student Success Dashboard</h1>
<h3 align="center">GenAI-powered Academic Mentor • RAG • ChromaDB • LangChain • Groq / Ollama</h3>

---

## 🚀 Overview
The **Smart Student Success Dashboard** is an AI-powered academic performance platform that enables students to monitor their attendance, marks, GPA trends, and receive **personalized recommendations** from a **GenAI Mentor** powered by **RAG** (Retrieval-Augmented Generation).  
It provides context-aware insights based on real student data, not generic AI responses.

---

## 🧠 Key Features
| Feature | Description |
|--------|------------|
| 🔐 Student Login | Simple authentication (ID = password for demo) |
| 📊 Dashboard Analytics | Attendance, marks, charts, performance KPIs |
| 📉 Attendance Insights | Class requirements to reach threshold |
| 🎯 Weak Subject Detection | Topic-based improvement suggestions |
| 🤖 GenAI Mentor | Personalized responses based on RAG |
| 🧠 Intent-aware queries | “Fix attendance”, “Improve DBMS”, “Make study plan” |
| 🗂 Digital Library | Recommended PDFs, notes, YouTube playlists |
| 🗓 Event Suggestions | Smart academic event recommendations |
| 🧩 LLM Agility | Switch between Groq / Gemeni / Ollama via `.env` |
| 🔁 Multi-student dataset | Different results for different profiles |

---

## 🧠 Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python, SQLAlchemy |
| Database | SQLite |
| Vector DB | ChromaDB |
| LLM | Groq (Llama-3.1-8B-Instant) / Ollama (Mistral) |
| Embeddings | nomic-embed-text |
| RAG Framework | LangChain |
| Architecture | Modular, Provider-agnostic AI Layer |

---

## 🏗 System Architecture
Streamlit UI (Dashboard + Chat)
|
Backend Controller
|
Student Data + Attendance + Marks (SQLite)
|
Context Builder → RAG Pipeline → LLM Response
(Dynamic context) (ChromaDB) (Groq / Ollama)


---

## 🔧 Installation & Setup

### 1️⃣ Clone repository
```bash
git clone https://github.com/suhasthadaka22/smart-student-success-dashboard.git
cd smart-student-success-dashboard
```
### 2️⃣ Setup Virtual Environment
```bash
pip install -r requirements.txt
```
### 3️⃣ Install requirements
```bash
pip install -r requirements.txt
```
### 4️⃣ Configure .env
LLM_PROVIDER=groq
EMBED_PROVIDER=ollama

GROQ_API_KEY=YOUR_GROQ_KEY
GROQ_LLM_MODEL=llama-3.1-8b-instant

OLLAMA_LLM_MODEL=mistral
OLLAMA_EMBED_MODEL=nomic-embed-text

### 5️⃣ Run App
```bash
streamlit run frontend/app.py
```

### 📸 Screenshots
![alt text](images/Log_in.png)
![alt text](images/Dashboard.png)
![alt text](images/Attendance.png)
![alt text](images/Marks.png) 
![alt text](images/GPA_Trend.png)   
![alt text](images/Lib+Events.png)
![alt text](images/Mentor_Response.png)

### 🧪 Example Queries to Try
| Question                            | Purpose                             |
| ----------------------------------- | ----------------------------------- |
| `Fix my attendance`                 | Attendance plan & class requirement |
| `Help me improve DBMS`              | Subject-weakness guidance           |
| `Make a 7-day study plan`           | Structured study roadmap            |
| `Summarize my academic performance` | Instant progress analysis           |
| `What CGPA can I target?`           | Motivation and prediction           |

### 🧱 Future Enhancements

Admin & Faculty portals

Hybrid search (BM25 + embeddings)

RAG evaluation & guardrails

Docker & cloud deployment

Notification & timetable module

Voice AI assistant

### 💼 Author

T. Suhas
AI/ML Engineer | GenAI Developer | Full-Stack Enthusiast
📍 Hyderabad, India
🔗 LinkedIn: https://linkedin.com/in/suhas-thadaka

⭐ Portfolio launching soon

###⭐ Support

If you like this project, consider starring ⭐ the repo — it helps visibility and motivates development! 🙌

###🌟 Final Note

This project demonstrates practical GenAI engineering with real-world RAG workflows and structured academic insight automation. Built for learning, portfolio value, and interview demonstration.