import streamlit as st
import PyPDF2
from groq import Groq

# ===============================
# 🔑 Config (Groq API Key)
# ===============================
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ===============================
# 📄 PDF Reader
# ===============================
def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# ===============================
# 📊 Resume Analyzer (Keyword Matching)
# ===============================
def analyze_resume(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    score = round((len(matched) / len(jd_words)) * 100, 2) if jd_words else 0

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }

# ===============================
# 🤖 Groq AI Feedback
# ===============================
def groq_feedback(resume_text, jd_text):
    prompt = f"""
    You are a resume expert. Compare this resume with the job description.

    Resume: {resume_text[:2000]}
    Job Description: {jd_text[:2000]}

    Provide a structured report with:
    1. Weak points in resume
    2. Missing important skills
    3. Suggestions for improvement
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192"
    )

    return response.choices[0].message.content

# ===============================
# 🎨 Streamlit UI
# ===============================
st.set_page_config(page_title="Resume Keyword Optimizer", layout="wide")
st.title("📄 Resume Keyword Optimizer")

jd_text = st.text_area("Paste Job Description here:", height=200)
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file and jd_text:
    with st.spinner("Analyzing Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        analysis = analyze_resume(resume_text, jd_text)
        feedback = groq_feedback(resume_text, jd_text)

    st.subheader("📊 Resume Match Score")
    st.metric("Score", f"{analysis['score']}%")

    st.subheader("✅ Matched Skills")
    st.write(", ".join(list(analysis["matched_skills"])) or "None")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(list(analysis["missing_skills"])) or "None")

    st.subheader("🤖 AI Suggestions (Groq)")
    st.write(feedback)
