# 📘 AI Smart Document Assistant

An intelligent AI-powered document assistant that can analyze multiple document types, generate summaries, answer questions, and provide context-aware recommendations.

## 🚀 Features

### 📄 Multi-Document Support
Upload and analyze:

- PDF (.pdf)
- Word Documents (.docx)
- Text Files (.txt)
- CSV Files (.csv)
- Excel Files (.xlsx)

---

### 🤖 AI-Powered Capabilities

#### 1. Document Summarization
- Generates concise summaries of uploaded documents.
- Highlights key points and important information.

#### 2. Question Answering
Ask natural language questions such as:

- "What are Saiful's updates?"
- "Who is on leave next week?"
- "What are the key findings in this report?"

The assistant searches relevant content and provides accurate answers.

#### 3. Smart Suggestions
Based on document type, AI provides recommendations.

Examples:

##### Health Reports
- Deficiency detection
- Diet recommendations
- Lifestyle suggestions
- Improvement areas

##### Resume Analysis
- ATS improvement suggestions
- Missing skills identification
- Interview preparation questions
- Career guidance

##### Employee Tracker
- Leave tracking
- Daily updates analysis
- Team insights
- Pending work identification

---

## 🧠 Intelligent Document Classification

The system automatically detects document types:

- Health Report
- Resume
- Employee Tracker
- Finance
- Education
- Legal
- General Documents

This enables context-aware AI responses.

---

## 🏗️ Architecture

```text
User Uploads Documents
        │
        ▼
Text Extraction
(PDF/DOCX/TXT/CSV/XLSX)
        │
        ▼
Document Classification
        │
        ▼
Text Chunking
        │
        ▼
Relevant Context Retrieval
        │
        ▼
OpenAI GPT
        │
        ▼
Summary / Suggestions / Q&A
```

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI
- OpenAI GPT

### Libraries
- pandas
- pypdf
- python-docx
- openpyxl
- scikit-learn
- python-dotenv

---

## 📂 Project Structure

```text
AI-Smart-Document-Assistant/
│
├── app.py
├── rag_utils.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Ankur1666/ai-personal-learning-coach.git
cd ai-personal-learning-coach
```

### Create Virtual Environment

```bash
python -m venv aivenv
```

### Activate Virtual Environment

Windows:

```bash
aivenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 💡 Sample Questions

### Employee Tracker

```text
Who is on leave?
```

```text
Give me Saiful's updates.
```

```text
What are the blockers for the BLK team?
```

### Resume

```text
What skills are missing?
```

```text
Generate interview questions.
```

### Health Report

```text
Summarize my report.
```

```text
What diet should I follow?
```

```text
What deficiencies are detected?
```

---

## 🔮 Future Enhancements

- Vector Database (FAISS/Chroma)
- LangChain Integration
- Voice Assistant
- Chat History
- Team Dashboard
- Cloud Deployment
- Slack / Teams Integration

---

## 👨‍💻 Author

**Ankur Mishra**

Python Developer | AI Enthusiast | Hackathon Participant

GitHub:
https://github.com/Ankur1666

---

## 📜 License

This project is developed for learning, experimentation, and hackathon purposes.
