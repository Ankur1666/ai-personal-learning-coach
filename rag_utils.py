from pypdf import PdfReader
from docx import Document
import pandas as pd
import os
from openai import OpenAI

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- OPENAI ---------------- #

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------- READ PDF ---------------- #

def read_pdf(file):

    text = ""

    pdf_reader = PdfReader(file)

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ---------------- READ DOCX ---------------- #

def read_docx(file):

    doc = Document(file)

    text = "\n".join(
        [para.text for para in doc.paragraphs]
    )

    return text


# ---------------- READ TXT ---------------- #

def read_txt(file):

    try:
        return file.read().decode("utf-8")

    except:
        file.seek(0)

        return file.read().decode("latin-1")


# ---------------- READ CSV ---------------- #

def read_csv(file):

    try:

        df = pd.read_csv(
            file,
            encoding="utf-8",
            header=None
        )

    except:

        file.seek(0)

        df = pd.read_csv(
            file,
            encoding="latin-1",
            header=None
        )

    df = df.fillna("")

    return df.to_string(index=False)


# ---------------- READ EXCEL ---------------- #

def read_excel(file):

    excel_data = pd.read_excel(
        file,
        sheet_name=None,
        header=None
    )

    all_text = ""

    for sheet_name, df in excel_data.items():

        all_text += f"\n--- Sheet: {sheet_name} ---\n"

        df = df.fillna("")

        for row in df.values:

            clean_row = [
                str(cell).strip()
                for cell in row
                if str(cell).strip() != ""
            ]

            if clean_row:

                all_text += " | ".join(clean_row)

                all_text += "\n"

    return all_text


# ---------------- EXTRACT TEXT ---------------- #

def extract_text(uploaded_files):

    all_text = ""

    for file in uploaded_files:

        file.seek(0)

        file_name = file.name.lower()

        all_text += f"\n\n========== FILE: {file.name} ==========\n\n"

        try:

            if file_name.endswith(".pdf"):

                all_text += read_pdf(file)

            elif file_name.endswith(".docx"):

                all_text += read_docx(file)

            elif file_name.endswith(".txt"):

                all_text += read_txt(file)

            elif file_name.endswith(".xlsx"):

                all_text += read_excel(file)

            elif file_name.endswith(".csv"):

                all_text += read_csv(file)

        except Exception as e:

            all_text += f"\nERROR: {str(e)}\n"

    return all_text


# ---------------- CREATE CHUNKS ---------------- #

def create_chunks(text, chunk_size=1500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


# ---------------- SEARCH RELEVANT CHUNKS ---------------- #

def search_chunks(chunks, question, top_k=5):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        chunks + [question]
    )

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    scores = similarity.flatten()

    top_indices = scores.argsort()[-top_k:][::-1]

    relevant_chunks = [
        chunks[i]
        for i in top_indices
    ]

    return "\n".join(relevant_chunks)


# ---------------- DETECT DOCUMENT TYPE ---------------- #

def detect_document_type(text):

    prompt = f"""
    Identify the document type.

    Possible types:
    - health
    - resume
    - employee_tracker
    - finance
    - education
    - legal
    - general

    Return ONLY one word.

    Document:
    {text[:3000]}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()


# ---------------- GENERATE SUMMARY ---------------- #

def generate_summary(full_text, doc_type):

    if doc_type == "health":

        system_prompt = """
        You are an AI Health Assistant.

        Tasks:
        - Summarize report
        - Detect abnormalities
        - Suggest diet
        - Suggest lifestyle improvements
        - Explain deficiencies simply
        """

    elif doc_type == "resume":

        system_prompt = """
        You are an AI Resume Coach.

        Tasks:
        - Summarize resume
        - Suggest improvements
        - Suggest missing skills
        - Suggest ATS improvements
        - Generate interview preparation suggestions
        """

    elif doc_type == "employee_tracker":

        system_prompt = """
        You are an AI Team Operations Assistant.

        Tasks:
        - Summarize employee updates
        - Detect blockers
        - Detect leaves
        - Highlight pending work
        """

    else:

        system_prompt = """
        You are an AI Document Assistant.

        Tasks:
        - Summarize document
        - Highlight important points
        - Give intelligent suggestions
        """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": full_text[:12000]
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ---------------- ASK AI ---------------- #

def ask_ai(full_text, question, doc_type):

    chunks = create_chunks(full_text)

    relevant_context = search_chunks(
        chunks,
        question
    )

    if doc_type == "health":

        system_prompt = """
        You are an AI Health Assistant.

        Answer health-related questions clearly.
        Suggest diet and improvements if needed.
        """

    elif doc_type == "resume":

        system_prompt = """
        You are an AI Resume Coach.

        Answer resume-related questions.
        Suggest interview preparation tips.
        """

    elif doc_type == "employee_tracker":

        system_prompt = """
        You are an AI Team Operations Assistant.

        Answer questions about employee updates,
        blockers, leaves and tasks.
        """

    else:

        system_prompt = """
        You are an AI Smart Document Assistant.

        Answer user questions based on uploaded document.
        """

    final_prompt = f"""
    Context:
    {relevant_context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content